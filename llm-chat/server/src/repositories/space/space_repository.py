from src.models.space import Space
from src.core.config import storage_settings
from src.utils.decorators import singleton
from src.core.exceptions.space import SpaceError, SpaceNotFoundError, SpaceAlreadyExistsError
from src.repositories.base import BaseAzureBlobRepository
from .interfaces import ISpaceRepository
from typing import List

@singleton
class SpaceRepository(BaseAzureBlobRepository, ISpaceRepository):
    """Repository for managing spaces in azure blob storage"""

    def __init__(self):
        super().__init__(storage_settings.SPACE_CONTAINER_NAME)

    @staticmethod
    def _get_space_blob_name(space_name: str) -> str:
        """Get the blob name for space"""
        return f"spaces/{space_name}/_info.json"

    async def space_exists(self, space_name: str) -> bool:
        """Check if a space exists"""
        try:
            space_blob_name = self._get_space_blob_name(space_name)
            return await self._blob_exists(space_blob_name)
        except Exception as e:
            raise SpaceError(f"Failed to check space existence: {str(e)}")

    async def create_new_space(self, space: Space) -> Space:
        """Create a new space with space info"""
        try:
            space_blob_name = self._get_space_blob_name(space.name)
            await self._upload_json(
                blob_name=space_blob_name,
                data=space.model_dump_json(indent=2),
                overwrite=False
            )
            return space
        except Exception as e:
            raise SpaceError(f"Failed to create space: {str(e)}")

    async def get_by_name(self, space_name: str) -> Space:
        """Get a space by name"""
        try:
            blob_name = self._get_space_blob_name(space_name)
            data = await self._download_json(blob_name)
            existing_space = Space.model_validate_json(data)
            return existing_space
        except SpaceError:
            raise
        except Exception as e:
            raise SpaceError(f"Failed to get space: {str(e)}")

    async def list_all_spaces(self) -> List[Space]:
        """List all spaces"""
        try:
            spaces = []
            async for blob in self._container_client.walk_blobs(
                name_starts_with="spaces/",
                delimiter="/files"      # TODO: handle cases with subdirectories
            ):
                if blob.name != "spaces/_info.json":  # Skip directory info
                    data = await self._download_json(blob.name)
                    space = Space.model_validate_json(data)
                    spaces.append(space)
            return spaces
        except Exception as e:
            raise SpaceError(f"Failed to list spaces: {str(e)}")

    async def delete_by_name(self, space_name: str) -> None:
        """
        Delete a space by name

        Note: This will delete space info and all files in the space.
        """
        try:
            blob_name = self._get_space_blob_name(space_name)
            await self._delete_blob(blob_name)

            # Delete all files in space
            async for blob in self._container_client.walk_blobs(
                name_starts_with=f"spaces/{space_name}/"
            ):
                await self._delete_blob(blob.name)
        except Exception as e:
            raise SpaceError(f"Failed to delete space: {str(e)}")