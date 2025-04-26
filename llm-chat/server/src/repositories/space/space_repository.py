from src.models.space import Space
from src.core.config import storage_settings
from src.utils.decorators import singleton
from src.core.exceptions.space import SpaceError, SpaceNotFoundError, SpaceAlreadyExistsError
from src.repositories.base import BaseAzureBlobRepository
from .space_directory import SpaceDirectoryManager
from .interfaces import ISpaceRepository
from typing import List

@singleton
class SpaceRepository(BaseAzureBlobRepository, ISpaceRepository):
    """Repository for managing spaces in azure blob storage"""

    def __init__(self):
        super().__init__(storage_settings.SPACE_CONTAINER_NAME)
        self._directory_manager = SpaceDirectoryManager()

    async def _async_init(self) -> None:
        """Initialize async components"""
        await self._ensure_initialized()
        await self._directory_manager.ensure_directory_exists()

    @staticmethod
    def _space_info_blob_name(space_name: str) -> str:
        """Get the blob name for space info"""
        return f"spaces/{space_name}/_info.json"

    async def create(self, space: Space) -> Space:
        """Create a new space"""
        return await self.create_space_info(space)

    async def get(self, space_id: str) -> Space:
        """Get a space by ID"""
        # Implementation needed - you might want to maintain an ID to name mapping
        raise NotImplementedError("Get by ID not implemented")

    async def create_space_info(self, space: Space) -> Space:
        """Create a new space with space info"""
        try:
            await self._async_init()
            blob_name = self._space_info_blob_name(space.name)

            if await self._blob_exists(blob_name):
                raise SpaceAlreadyExistsError(f"Space with name '{space.name}' already exists")

            await self._directory_manager.add_space(space)
            await self._upload_json(
                blob_name,
                space.model_dump_json(indent=2),
                overwrite=False
            )
            return space
        except SpaceError:
            raise
        except Exception as e:
            raise SpaceError(f"Failed to create space: {str(e)}")

    async def get_by_name(self, space_name: str) -> Space:
        """Get a space by name"""
        try:
            await self._async_init()
            blob_name = self._space_info_blob_name(space_name)

            if not await self._blob_exists(blob_name):
                raise SpaceNotFoundError(f"Space '{space_name}' not found")

            data = await self._download_json(blob_name)
            return Space.model_validate_json(data)
        except SpaceError:
            raise
        except Exception as e:
            raise SpaceError(f"Failed to get space: {str(e)}")

    async def delete(self, space_id: str) -> None:
        """Delete a space by ID"""
        # Implementation needed - you might want to maintain an ID to name mapping
        raise NotImplementedError("Delete by ID not implemented")

    async def delete_by_name(self, space_name: str) -> None:
        """Delete a space by name"""
        try:
            await self._async_init()
            blob_name = self._space_info_blob_name(space_name)

            if not await self._blob_exists(blob_name):
                return

            await self._directory_manager.remove_space(space_name)
            await self._delete_blob(blob_name)

            # Delete all files in space
            async for blob in self._container_client.list_blobs(
                name_starts_with=f"spaces/{space_name}/"
            ):
                await self._delete_blob(blob.name)
        except Exception as e:
            raise SpaceError(f"Failed to delete space: {str(e)}")

    async def list(self) -> list[Space]:
        """List all spaces"""
        return await self.list_all_spaces_info()

    async def list_all_spaces_info(self) -> List[Space]:
        """List all spaces"""
        try:
            await self._async_init()
            spaces = []
            async for blob in self._container_client.walk_blobs(
                name_starts_with="spaces/",
                delimiter="_info.json"
            ):
                if blob.name != "spaces/_info.json":  # Skip directory info
                    data = await self._download_json(blob.name)
                    space = Space.model_validate_json(data)
                    spaces.append(space)
            return spaces
        except Exception as e:
            raise SpaceError(f"Failed to list spaces: {str(e)}")

    async def exists(self, space_name: str) -> bool:
        """Check if a space exists"""
        try:
            await self._async_init()
            blob_name = self._space_info_blob_name(space_name)
            return await self._blob_exists(blob_name)
        except Exception as e:
            raise SpaceError(f"Failed to check space existence: {str(e)}")