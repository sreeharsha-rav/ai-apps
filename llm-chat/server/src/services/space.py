from src.models.space import Space
from src.schemas.space import SpaceRequest, SpaceResponse
from src.repositories.space import SpaceRepository, SpaceDirectoryManager
from src.repositories.file import FileDirectoryManager
from src.utils.decorators import singleton
from src.core.exceptions.space import SpaceError, SpaceNotFoundError, SpaceAlreadyExistsError

@singleton
class SpaceService:
    """Service for managing spaces."""

    def __init__(self):
        """Initialize the SpaceService"""
        self._space_repository = SpaceRepository()
        self._space_directory_manager = SpaceDirectoryManager()
        self._file_directory_manager = FileDirectoryManager()

    async def create_new_space(self, space_request: SpaceRequest) -> SpaceResponse:
        """Create a space from a space request"""
        try:
            space = Space(
                name=space_request.name,
                description=space_request.description,
            )

            # check if spaces directory exists, create if not
            if not await self._space_directory_manager.spaces_dir_exists():
                await self._space_directory_manager.create_spaces_dir()

            # check if space already exists, throw if it does
            if await self._space_repository.space_exists(space.name):
                raise SpaceAlreadyExistsError(f"Space with name '{space.name}' already exists")

            # create space
            created_space = await self._space_repository.create_new_space(space)

            # check if files directory exists, create if not
            if not await self._file_directory_manager.files_dir_exists(space.name):
                await self._file_directory_manager.create_files_dir(space.name)

            return SpaceResponse(
                space_id=created_space.space_id,
                name=created_space.name,
                description=created_space.description,
                files=[],
                created_at=created_space.created_at,
                updated_at=created_space.updated_at,
            )
        except SpaceAlreadyExistsError:
            raise
        except Exception as e:
            raise SpaceError(f"Failed to create space: {str(e)}")

    async def get_space_by_name(self, space_name: str) -> SpaceResponse:
        """Get a space by name"""
        try:
            # check if space exists
            if not await self._space_repository.space_exists(space_name):
                raise SpaceNotFoundError(f"Space with name '{space_name}' not found")

            # get space metadata
            space = await self._space_repository.get_by_name(space_name)
            # TODO:get files metadata in space

            return SpaceResponse(
                space_id=space.space_id,
                name=space.name,
                description=space.description,
                files=[],       # TODO
                created_at=space.created_at,
                updated_at=space.updated_at,
            )
        except SpaceNotFoundError:
            raise
        except Exception as e:
            raise SpaceError(f"Failed to get space: {str(e)}")

    async def list_all_spaces(self) -> list[SpaceResponse]:
        """List all spaces"""
        try:
            spaces = await self._space_repository.list_all_spaces()
            # TODO: get files metadata in each space
            return [SpaceResponse(
                space_id=space.space_id,
                name=space.name,
                description=space.description,
                files=[],       # TODO
                created_at=space.created_at,
                updated_at=space.updated_at,
            ) for space in spaces]
        except Exception as e:
            raise Exception(f"Failed to list spaces: {str(e)}")

    async def delete_space_by_name(self, space_name: str) -> None:
        """Delete a space by name"""
        try:
            # NOTE: this will delete space and all files in space and files directory
            await self._space_repository.delete_by_name(space_name)
        except Exception as e:
            raise Exception(f"Failed to delete space: {str(e)}")