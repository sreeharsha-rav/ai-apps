from src.models.space import SpacesDir, Space, SpaceBase
from src.repositories.base import BaseAzureBlobRepository
from src.core.config import storage_settings
from .interfaces import ISpaceDirectoryManager

class SpaceDirectoryManager(BaseAzureBlobRepository, ISpaceDirectoryManager):
    """Manager for space directory operations"""

    def __init__(self):
        super().__init__(storage_settings.SPACE_CONTAINER_NAME)
        self._spaces_dir_blob = "spaces/_info.json"

    async def spaces_dir_exists(self) -> bool:
        """Check if spaces directory exists"""
        return await self._blob_exists(self._spaces_dir_blob)

    async def create_spaces_dir(self) -> None:
        """Ensure spaces directory exists"""
        try:
            await self._upload_json(
                self._spaces_dir_blob,
                SpacesDir().model_dump_json(indent=2),
                overwrite=False
            )
        except Exception as e:
            raise Exception(f"Failed to ensure directory exists: {str(e)}")

    async def add_space_to_spaces_info(self, space: Space) -> None:
        """Add space to directory"""
        try:
            data = await self._download_json(self._spaces_dir_blob)
            spaces_dir = SpacesDir.model_validate_json(data)
            spaces_dir.spaces.append(SpaceBase(
                space_id=space.space_id,
                name=space.name,
            ))
            await self._upload_json(
                self._spaces_dir_blob,
                spaces_dir.model_dump_json(indent=2),
                overwrite=True
            )
        except Exception as e:
            raise Exception(f"Failed to add space to directory: {str(e)}")

    async def remove_space_from_spaces_info(self, space_name: str) -> None:
        """Remove space from directory"""
        try:
            data = await self._download_json(self._spaces_dir_blob)
            spaces_dir = SpacesDir.model_validate_json(data)
            spaces_dir.spaces = [s for s in spaces_dir.spaces if s.name != space_name]
            await self._upload_json(
                self._spaces_dir_blob,
                spaces_dir.model_dump_json(indent=2),
                overwrite=True
            )
        except Exception as e:
            raise Exception(f"Failed to remove space from directory: {str(e)}")