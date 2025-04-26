from src.models.file import File, FilesDir
from src.repositories.base import BaseAzureBlobRepository
from src.repositories.file.interfaces import IFileDirectoryManager
from src.core.config import storage_settings

class FileDirectoryManager(BaseAzureBlobRepository, IFileDirectoryManager):
    """Manager for file directory operations"""

    def __init__(self):
        super().__init__(storage_settings.SPACE_CONTAINER_NAME)

    @staticmethod
    def _get_files_dir_blob(space_name: str) -> str:
        """Get the blob name for files directory"""
        return f"spaces/{space_name}/files/_info.json"

    async def files_dir_exists(self, space_name: str) -> bool:
        """Check if files directory exists"""
        try:
            files_dir_blob = self._get_files_dir_blob(space_name)
            return await self._blob_exists(files_dir_blob)
        except Exception as e:
            raise Exception(f"Failed to check directory existence: {str(e)}")

    async def create_files_dir(self, space_name: str) -> None:
        """Create files directory"""
        try:
            files_dir_blob = self._get_files_dir_blob(space_name)
            await self._upload_json(
                files_dir_blob,
                FilesDir().model_dump_json(indent=2),
                overwrite=False
            )
        except Exception as e:
            raise Exception(f"Failed to ensure directory exists: {str(e)}")

    async def add_file_to_files_info(self, space_name: str, file: File) -> None:
        """Add file to directory"""
        try:
            files_dir_blob = self._get_files_dir_blob(space_name)
            data = await self._download_json(files_dir_blob)
            files_dir = FilesDir.model_validate_json(data)
            files_dir.files.append(file)
            await self._upload_json(
                files_dir_blob,
                files_dir.model_dump_json(indent=2),
                overwrite=True
            )
        except Exception as e:
            raise Exception(f"Failed to add file to directory: {str(e)}")

    async def remove_file_from_files_info(self, space_name: str, file: File) -> None:
        """Remove file from directory"""
        try:
            files_dir_blob = self._get_files_dir_blob(space_name)
            data = await self._download_json(files_dir_blob)
            files_dir = FilesDir.model_validate_json(data)
            files_dir.files = [f for f in files_dir.files if f.file_id != file.file_id]
            await self._upload_json(
                files_dir_blob,
                files_dir.model_dump_json(indent=2),
                overwrite=True
            )
        except Exception as e:
            raise Exception(f"Failed to remove file from directory: {str(e)}")