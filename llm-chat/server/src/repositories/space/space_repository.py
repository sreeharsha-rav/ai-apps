from src.models.space import Space
from src.core.config import storage_settings
from src.utils.decorators import singleton
from .interfaces import ISpaceRepository
from azure.storage.blob.aio import ContainerClient, BlobClient
from typing import List

@singleton
class SpaceRepository(ISpaceRepository):
    """Repository for managing spaces in azure blob storage"""

    def __init__(self):
        self._space_container_client = ContainerClient.from_connection_string(
            conn_str=storage_settings.AZURE_STORAGE_CONNECTION_STRING,
            container_name=storage_settings.SPACE_CONTAINER_NAME
        )

    def _get_space_blob_client(self, space_name: str) -> BlobClient:
        """Get the blob name for space"""
        space_blob_name = f"spaces/{space_name}/_info.json"
        space_blob_client = self._space_container_client.get_blob_client(blob=space_blob_name)
        return space_blob_client

    async def space_exists(self, space_name: str) -> bool:
        """Check if a space exists"""
        space_blob_client = self._get_space_blob_client(space_name)
        return await space_blob_client.exists()

    async def create_new_space(self, space: Space) -> Space:
        """Create a new space with space info"""
        space_blob_client = self._get_space_blob_client(space.name)
        await space_blob_client.upload_blob(
            data="b{}",
            metadata=space.model_dump(),
            overwrite=False
        )
        return space

    async def get_by_name(self, space_name: str) -> Space:
        """Get a space by name"""
        space_blob_client = self._get_space_blob_client(space_name)
        space_blob_properties = await space_blob_client.get_blob_properties()
        space_blob_metadata = space_blob_properties.metadata
        space = Space(**space_blob_metadata)
        return space

    async def list_all_spaces(self) -> List[Space]:
        """List all spaces"""
        spaces = []
        async for blob in self._space_container_client.walk_blobs(
            name_starts_with="spaces/",
            delimiter="/files"      # TODO: handle cases with subdirectories
        ):
            if blob.name != "spaces/_info.json":  # Skip directory info
                space_blob_client = self._space_container_client.get_blob_client(blob=blob.name)
                space_blob_properties = await space_blob_client.get_blob_properties()
                space_blob_metadata = space_blob_properties.metadata
                space = Space(**space_blob_metadata)
                spaces.append(space)
        return spaces

    async def delete_by_name(self, space_name: str) -> None:
        """
        Delete a space by name

        Note: This will delete space info and all files in the space.
        """
        space_blob_client = self._get_space_blob_client(space_name)
        await space_blob_client.delete_blob()

        # Delete all files in space
        async for blob in self._space_container_client.walk_blobs(
            name_starts_with=f"spaces/{space_name}/"
        ):
            space_blob_client = self._space_container_client.get_blob_client(blob=blob.name)
            await space_blob_client.delete_blob()