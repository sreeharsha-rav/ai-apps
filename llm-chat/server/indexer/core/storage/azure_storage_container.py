from azure.storage.blob.aio import ContainerClient, BlobClient
from .base_storage import BaseStorage
from indexer.config import azure_storage_settings
from indexer.schemas.metadata import SpaceMetadata
from indexer.schemas.document import RawDocument
from indexer.utils.logging import setup_logger
from typing import AsyncGenerator

class AzureStorageContainer(BaseStorage):
    """Class for interacting with Azure Blob Storage container."""

    def __init__(self, user_id):
        """
        Initialize the Azure Storage container.

        Args:
            user_id: Unique user identifier for container
        """
        try:
            self.user_id = user_id
            self.logger = setup_logger(name="Indexer: azure_storage")
            self.logger.info(f"Initializing Azure Storage container for user: {user_id}")
            
            self.container_client = ContainerClient.from_connection_string(
                conn_str=azure_storage_settings.AZURE_STORAGE_CONNECTION_STRING,
                container_name=f"{self.user_id}-container"
            )

            self.logger.debug(f"Azure Storage container initialized successfully")

        except Exception as e:
            self.logger.error(f"Error initializing Azure Storage container: {str(e)}")
            raise e

    async def _get_space_blob_client(self, space_name: str) -> BlobClient:
        """
        Get a blob client for the specified space.

        Args:
            space_name: Space name to get blob for

        Returns:
            Blob client for the specified space
        """
        try:
            blob_name = f"spaces/{space_name}/_info.json"       # adjust this accordingly
            self.logger.debug(f"Getting blob client for {blob_name}")
            blob_client = self.container_client.get_blob_client(blob=blob_name)

            # check if blob exists
            if not await blob_client.exists():
                raise Exception("Blob does not exist")

            return blob_client
        except Exception as e:
            print(f"Error getting blob client for {space_name}: {str(e)}")
            raise e

    async def does_space_exist(self, space_name: str) -> bool:
        """
        Check if a space exists.

        Args:
            space_name: Space name

        Returns:
            True if the space exists, False otherwise
        """
        try:
            blob_client = await self._get_space_blob_client(space_name)
            return await blob_client.exists()
        except Exception as e:
            self.logger.error(f"Error checking if space exists: {str(e)}")
            raise e

    async def get_space_metadata(self, space_name: str) -> SpaceMetadata:
        """
        Get the metadata for a space.

        Args:
            space_name: Space name

        Returns:
            Space metadata object
        """
        try:
            # get blob client
            blob_client = await self._get_space_blob_client(space_name)

            # get metadata from blob properties
            blob_properties = await blob_client.get_blob_properties()
            blob_metadata = blob_properties.metadata

            # validate metadata using pydantic
            space_metadata = SpaceMetadata.model_validate(blob_metadata)
            return space_metadata
        except Exception as e:
            print(f"Error getting metadata for {space_name}: {str(e)}")
            raise e

    async def update_space_metadata(self, space_name: str, metadata: SpaceMetadata):
        """
        Update the metadata for a space.

        Args:
            space_name: Space name
            metadata: space metadata object
        """
        try:
            blob_client = await self._get_space_blob_client(space_name)
            await blob_client.upload_blob(
                data="b{}",
                metadata=metadata.model_dump(),
                overwrite=True
            )
        except Exception as e:
            print(f"Error updating metadata for {space_name}: {str(e)}")
            raise e

    async def list_all_files(self, space_name: str) -> list[str]:
        """
        List all files in a space.

        Args:
            space_name: Space name

        Returns:
            List of file names in the space
        """
        try:
            files = []
            prefix = f"spaces/{space_name}/files/"

            async for blob in self.container_client.walk_blobs(name_starts_with=prefix):
                # Skip directories/prefixes
                if hasattr(blob, 'name'):  # Only process actual blobs, not prefixes
                    file_name = blob.name.split("/")[-1]

                    # Skip metadata files
                    if file_name == "_info.json":
                        continue

                    files.append(file_name)
            return files
        except Exception as e:
            print(f"Error listing files in {space_name}: {str(e)}")
            raise e

    def load_all_files(self, space_name: str, files: list[str]) -> AsyncGenerator[RawDocument, None]:
        """
        Load all files in a space as an async generator.

        Args:
            space_name: Space name
            files: List of file names in the space
            
        Returns:
            AsyncGenerator of RawDocument objects
        """
        async def _load_files():
            try:
                for idx, file in enumerate(files, 1):
                    blob_path = f"spaces/{space_name}/files/{file}"
                    extension = file.split(".")[-1]
                    blob_client = self.container_client.get_blob_client(blob=blob_path)

                    self.logger.info(f"Downloading {idx}/{len(files)}: {blob_path}")

                    stream = await blob_client.download_blob()
                    content = await stream.readall()
                    yield RawDocument(
                        user_id=self.user_id,
                        space_name=space_name,
                        file_name=file,
                        file_extension=extension,
                        blob_path=blob_path,
                        content=content,
                    )

            except Exception as e:
                self.logger.error(f"Error loading documents from {space_name}: {str(e)}")
                raise e
                
        return _load_files()
