from fastapi import UploadFile
from src.models.file import File, FileExtension
from src.repositories.file import FileRepository, FileDirectoryManager
from src.repositories.space import SpaceRepository
from src.core.exceptions.file import FileError
from src.schemas.file import FileResponse, FileRequest
from src.utils.decorators import singleton
from src.utils.loggers import setup_logger

@singleton
class FileService:
    """Service for managing files within spaces"""

    def __init__(self):
        self._space_repository = SpaceRepository()
        self._file_repository = FileRepository()
        self._file_directory_manager = FileDirectoryManager()
        self.logger = setup_logger(name="file_service")

    async def upload_file(self, space_name: str, file_data: UploadFile) -> FileResponse:
        """Upload a file to a space"""
        try:
            self.logger.info(f"Uploading file '{file_data.filename}' to space: {space_name}")
            # Check if files directory exists, create if not
            if not await self._file_directory_manager.files_dir_exists(space_name):
                raise FileError(f"Files directory does not exist for space '{space_name}'")

            # Create new file model
            file_name, file_extension = file_data.filename.rsplit('.', 1)
            new_file = File(
                base_name=file_name,
                extension=FileExtension(file_extension),  # extension validated in advance by client
            )

            # check if file already exists
            if await self._file_repository.file_exists(
                space_name=space_name,
                file_name=new_file.base_name,
                file_extension=new_file.extension
            ):
                raise FileError(f"File '{new_file.base_name}.{new_file.extension}' already exists in space '{space_name}'")

            # TODO: validate file extension in UploadFile
            # TODO: validate file size in UploadFile
            # TODO: validate file name in UploadFile

            # Read file content
            content = await file_data.read()

            # Upload to storage
            await self._file_repository.upload_file(
                space_name=space_name,
                file=new_file,
                content=content
            )

            # Create response
            response = FileResponse(
                file_id=new_file.file_id,
                base_name=new_file.base_name,
                extension=new_file.extension,
                created_at=new_file.created_at,
                updated_at=new_file.updated_at,
            )
            self.logger.info(f"Successfully uploaded file '{file_data.filename}' to space: {space_name}")
            return response
        except FileError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to upload file '{file_data.filename}' to space '{space_name}': {str(e)}")
            raise FileError(f"Failed to upload file: {str(e)}")

    async def get_file(self, space_name: str, file: FileRequest) -> FileResponse:
        """Get file metadata"""
        try:

            # check if file exists
            if not await self._file_repository.file_exists(
                space_name=space_name,
                file_name=file.base_name,
                file_extension=file.extension
            ):
                raise FileError(f"File '{file.base_name}.{file.extension}' does not exist in space '{space_name}'")

            file = await self._file_repository.get_file_by_name(
                space_name=space_name,
                file_name=file.base_name,
                file_extension=file.extension
            )

            return FileResponse(**file.model_dump())
        except FileError:
            raise
        except Exception as e:
            raise Exception(f"Failed to get file: {str(e)}")

    async def list_all_files(self, space_name: str) -> list[FileResponse]:
        """List all files in a space"""
        try:
            self.logger.info(f"Listing all files in space: {space_name}")
            # check if files directory exists
            if not await self._file_directory_manager.files_dir_exists(space_name):
                raise FileError(f"Files directory does not exist for space '{space_name}'")

            files = await self._file_repository.list_all_files(space_name)
            self.logger.info(f"Successfully listed {len(files)} files in space: {space_name}")
            return [
                FileResponse(**file.model_dump())
                for file in files
            ]
        except FileError:
            raise
        except Exception as e:
            self.logger.error(f"Failed to list files in space '{space_name}': {str(e)}")
            raise Exception(f"Failed to list files: {str(e)}")

    async def delete_file(self, space_name: str, file: FileRequest) -> None:
        """Delete a file from a space"""
        try:
            # check if file exists
            if await self._file_repository.file_exists(
                space_name=space_name,
                file_name=file.base_name,
                file_extension=file.extension
            ):
                # delete file from storage
                await self._file_repository.delete_file_by_name(
                    space_name=space_name,
                    file_name=file.base_name,
                    file_extension=file.extension
                )
        except FileError:
            raise
        except Exception as e:
            raise Exception(f"Failed to delete file: {str(e)}")