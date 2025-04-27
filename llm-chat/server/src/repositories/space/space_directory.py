from src.core.config import storage_settings
from .interfaces import ISpaceDirectoryManager
from azure.storage.blob.aio import BlobClient

class SpaceDirectoryManager(ISpaceDirectoryManager):
    """Manager for space directory operations"""

    def __init__(self):
        self._spaces_dir_blob = "spaces/_info.json"
        self._spaces_dir_blob_client = BlobClient.from_connection_string(
            conn_str=storage_settings.AZURE_STORAGE_CONNECTION_STRING,
            container_name=storage_settings.SPACE_CONTAINER_NAME,
            blob_name=self._spaces_dir_blob
        )

    async def spaces_dir_exists(self) -> bool:
        """Check if spaces directory exists"""
        return await self._spaces_dir_blob_client.exists()

    async def create_spaces_dir(self) -> None:
        """Ensure spaces directory exists"""
        await self._spaces_dir_blob_client.upload_blob(
            data="b{}",                             # create an empty blob to represent the directory
            tags={
                "category": "spaces"                # create a tag for spaces directory
            },
            overwrite=False
        )