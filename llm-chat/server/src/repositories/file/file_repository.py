from src.models.file import File, FileExtension
from .interfaces import IFileRepository
from src.core.config import storage_settings
from src.utils.decorators import singleton
from azure.storage.blob.aio import ContainerClient, BlobClient
from src.utils.loggers import setup_logger
from src.core.exceptions.file import FileError, FileNotFoundError, FileAlreadyExistsError

@singleton
class FileRepository(IFileRepository):
    """Repository for managing files under spaces in azure blob storage"""

    def __init__(self):
        """Initialize the FileRepository"""
        self.logger = setup_logger(name="file_repository")
        self._space_container_client = ContainerClient.from_connection_string(
            conn_str=storage_settings.AZURE_STORAGE_CONNECTION_STRING,
            container_name=storage_settings.SPACE_CONTAINER_NAME
        )
        self.logger.info("FileRepository initialized")

    def _get_file_blob_client(self, space_name: str, file_name: str, file_extension: FileExtension) -> BlobClient:
        """Get the blob client for a file within a space"""
        file_blob_name = f"spaces/{space_name}/files/{file_name}.{file_extension.value}"
        self.logger.debug(f"Getting blob client for file: {file_blob_name}")
        return self._space_container_client.get_blob_client(blob=file_blob_name)

    async def file_exists(self, space_name: str, file_name: str, file_extension: FileExtension) -> bool:
        """Check if a file exists in a space"""
        try:
            self.logger.debug(f"Checking if file '{file_name}.{file_extension.value}' exists in space: {space_name}")
            file_blob_client = self._get_file_blob_client(space_name, file_name, file_extension)
            exists = await file_blob_client.exists()
            self.logger.debug(f"File '{file_name}.{file_extension.value}' exists: {exists}")
            return exists
        except Exception as e:
            self.logger.error(f"Error checking file existence '{file_name}.{file_extension.value}' in space '{space_name}': {str(e)}")
            raise FileError(f"Failed to check file existence: {str(e)}")

    async def upload_file(self, space_name: str, file: File, content: bytes) -> File:
        """Upload a file to a space"""
        try:
            self.logger.info(f"Uploading file '{file.base_name}.{file.extension.value}' to space: {space_name}")
            file_blob_client = self._get_file_blob_client(space_name, file.base_name, file.extension)
            
            # Check if file already exists
            if await file_blob_client.exists():
                self.logger.warning(f"File '{file.base_name}.{file.extension.value}' already exists in space '{space_name}'")
                raise FileAlreadyExistsError(f"File '{file.base_name}.{file.extension.value}' already exists")

            await file_blob_client.upload_blob(
                data=content,
                metadata=file.model_dump(),
                overwrite=False
            )
            self.logger.info(f"Successfully uploaded file '{file.base_name}.{file.extension.value}' to space: {space_name}")
            return file
        except FileAlreadyExistsError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to upload file '{file.base_name}.{file.extension.value}' to space '{space_name}': {str(e)}")
            raise FileError(f"Failed to upload file: {str(e)}")

    async def get_file_by_name(self, space_name: str, file_name: str, file_extension: FileExtension) -> File:
        """Get a file metadata from a space"""
        try:
            file_blob_client = self._get_file_blob_client(space_name, file_name, file_extension)
            
            # Check if file exists
            if not await file_blob_client.exists():
                self.logger.warning(f"File '{file_name}.{file_extension.value}' not found in space '{space_name}'")
                raise FileNotFoundError(f"File '{file_name}.{file_extension.value}' not found")

            file_properties = await file_blob_client.get_blob_properties()
            file_metadata = file_properties.metadata
            existing_file = File(**file_metadata)
            self.logger.info(f"Successfully retrieved file '{file_name}.{file_extension.value}' from space: {space_name}")
            return existing_file
        except FileNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to get file '{file_name}.{file_extension.value}' from space '{space_name}': {str(e)}")
            raise FileError(f"Failed to get file: {str(e)}")

    async def list_all_files(self, space_name: str) -> list[File]:
        """List all files in a space"""
        try:
            self.logger.info(f"Listing all files in space: {space_name}")
            files = []
            processed_files = set()  # Track processed files to avoid duplicates
            
            # List only files in the space's files directory
            async for blob in self._space_container_client.list_blobs(name_starts_with=f"spaces/{space_name}/files/"):
                # Parse the blob name to get file details
                parts = blob.name.split("/")
                if len(parts) == 4:  # Format: spaces/{space_name}/files/{filename}
                    file_full_name = parts[3]  # Get the full file name with extension
                    
                    # Skip if we've already processed this file
                    if file_full_name in processed_files:
                        self.logger.debug(f"Skipping duplicate file: {file_full_name}")
                        continue
                    
                    try:
                        self.logger.debug(f"Processing file: {file_full_name}")
                        file_blob_client = self._space_container_client.get_blob_client(blob=blob.name)
                        file_properties = await file_blob_client.get_blob_properties()
                        file_metadata = file_properties.metadata
                        
                        if file_metadata:  # Only process if metadata exists
                            file = File(**file_metadata)
                            files.append(file)
                            processed_files.add(file_full_name)
                            self.logger.debug(f"Successfully processed file: {file_full_name}")
                    except Exception as e:
                        self.logger.warning(f"Failed to process file '{file_full_name}' in space '{space_name}': {str(e)}")
                        continue

            self.logger.info(f"Successfully listed {len(files)} files in space: {space_name}")
            return files
        except Exception as e:
            self.logger.error(f"Failed to list files in space '{space_name}': {str(e)}")
            raise FileError(f"Failed to list files: {str(e)}")

    async def delete_file_by_name(self, space_name: str, file_name: str, file_extension: FileExtension) -> None:
        """Delete a file from a space"""
        try:
            self.logger.info(f"Deleting file '{file_name}.{file_extension.value}' from space: {space_name}")
            file_blob_client = self._get_file_blob_client(space_name, file_name, file_extension)
            
            # Check if file exists
            if not await file_blob_client.exists():
                self.logger.warning(f"File '{file_name}.{file_extension.value}' not found in space '{space_name}'")
                raise FileNotFoundError(f"File '{file_name}.{file_extension.value}' not found")

            await file_blob_client.delete_blob()
            self.logger.info(f"Successfully deleted file '{file_name}.{file_extension.value}' from space: {space_name}")
        except FileNotFoundError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to delete file '{file_name}.{file_extension.value}' from space '{space_name}': {str(e)}")
            raise FileError(f"Failed to delete file: {str(e)}")
