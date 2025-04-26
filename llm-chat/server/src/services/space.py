from src.models.space import Space
from src.schemas.space import SpaceRequest, SpaceResponse
from src.repositories.space import SpaceRepository
from src.utils.decorators import singleton
from src.core.exceptions.space import SpaceError

@singleton
class SpaceService:
    """Service for managing spaces."""

    def __init__(self):
        """Initialize the SpaceService"""
        self._space_repository = SpaceRepository()

    async def create_new_space(self, space_request: SpaceRequest) -> SpaceResponse:
        """Create a space from a space request"""
        try:
            space = Space(
                name=space_request.name,
                description=space_request.description,
            )
            created_space = await self._space_repository.create_space_info(space)
            return SpaceResponse(
                space_id=created_space.space_id,
                name=created_space.name,
                description=created_space.description,
                created_at=created_space.created_at,
                updated_at=created_space.updated_at,
            )
        except SpaceError:
            raise
        except Exception as e:
            raise SpaceError(f"Failed to create space: {str(e)}")

    async def get_space(self, space_name: str) -> SpaceResponse:
        """Get a space by name"""
        try:
            space = await self._space_repository.get_space_by_name(space_name)
            return SpaceResponse(
                space_id=space.space_id,
                name=space.name,
                description=space.description,
                created_at=space.created_at,
                updated_at=space.updated_at,
            )
        except SpaceError:
            raise
        except Exception as e:
            raise SpaceError(f"Failed to get space: {str(e)}")

    async def list_spaces(self) -> list[SpaceResponse]:
        """List all spaces"""
        try:
            spaces = await self._space_repository.list_all_spaces_info()
            return [SpaceResponse(
                space_id=space.space_id,
                name=space.name,
                description=space.description,
                created_at=space.created_at,
                updated_at=space.updated_at,
            ) for space in spaces]
        except Exception as e:
            raise Exception(f"Failed to list spaces: {str(e)}")

    async def delete_space(self, space_id: str) -> None:
        """Delete a space by ID"""
        try:
            await self._space_repository.delete_space_by_name(space_id)
        except Exception as e:
            raise Exception(f"Failed to delete space: {str(e)}")