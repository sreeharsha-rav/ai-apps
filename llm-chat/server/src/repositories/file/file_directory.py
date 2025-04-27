from src.repositories.file.interfaces import IFileDirectoryManager
from src.core.config import storage_settings
from azure.storage.blob.aio import ContainerClient, BlobClient

class FileDirectoryManager(IFileDirectoryManager):
    """Manager for file directory operations"""

    def __init__(self):
        self._space_container_client = ContainerClient.from_connection_string(
            conn_str=storage_settings.AZURE_STORAGE_CONNECTION_STRING,
            container_name=storage_settings.SPACE_CONTAINER_NAME
        )

    def _get_files_dir_blob_client(self, space_name: str) -> BlobClient:
        """Get the blob name for files directory"""
        files_dir_blob = f"spaces/{space_name}/files/_info.json"
        return self._space_container_client.get_blob_client(blob=files_dir_blob)

    async def files_dir_exists(self, space_name: str) -> bool:
        """Check if files directory exists"""
        files_dir_blob = self._get_files_dir_blob_client(space_name)
        return await files_dir_blob.exists()

    async def create_files_dir(self, space_name: str) -> None:
        """Create files directory"""
        files_dir_blob = self._get_files_dir_blob_client(space_name)
        await files_dir_blob.upload_blob(
            data="b{}",                         # empty blob to represent directory
            tags={
                "category": "space-files"       # tag to identify files directory
            },
            overwrite=False
        )