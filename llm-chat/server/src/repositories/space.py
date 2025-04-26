from src.models.space import SpaceBase, Space, SpacesDir
from src.core.config import storage_settings
from azure.storage.blob.aio import ContainerClient
from src.utils.decorators import singleton
from src.utils.loggers import setup_logger
from src.core.exceptions.space import SpaceError, SpaceNotFoundError, SpaceAlreadyExistsError

@singleton
class SpaceRepository:
    """Repository for managing spaces in azure blob storage"""

    def __init__(self):
        """Initialize the SpaceRepository"""
        self.logger = setup_logger(name="space_repository")
        self._space_container_client = ContainerClient.from_connection_string(
            conn_str=storage_settings.AZURE_STORAGE_CONNECTION_STRING,
            container_name=storage_settings.SPACE_CONTAINER_NAME
        )
        self._initialized = False

    async def _async_init(self) -> None:
        """Initialize async components"""
        if self._initialized:
            self.logger.debug("SpaceRepository already initialized")
            return

        try:
            self.logger.info("Starting async space repository initialization")
            # Check if container exists
            exists = await self._space_container_client.exists()
            if not exists:
                self.logger.error(f"Container '{storage_settings.SPACE_CONTAINER_NAME}' does not exist")
                raise Exception(f"Container '{storage_settings.SPACE_CONTAINER_NAME}' does not exist")
            
            # Check if spaces dir info exists, create if not
            if not await self._does_spaces_dir_info_exist():
                self.logger.info("Creating spaces directory info")
                await self._create_spaces_dir_info()
            
            self._initialized = True
        except Exception as e:
            raise Exception(f"Failed to initialize SpaceRepository: {str(e)}")

    async def _does_spaces_dir_info_exist(self) -> bool:
        """Check if spaces dir info exists"""
        self.logger.debug("Checking if spaces directory info exists")
        spaces_blob_client = self._space_container_client.get_blob_client(
            blob="spaces/_info.json"
        )
        exists = await spaces_blob_client.exists()
        self.logger.debug(f"Spaces directory info exists: {exists}")
        return exists

    async def _create_spaces_dir_info(self) -> None:
        """Create a spaces directory with _info.json if it does not exist"""
        try:
            spaces_blob_client = self._space_container_client.get_blob_client(
                blob="spaces/_info.json"
            )
            if not await spaces_blob_client.exists():
                await spaces_blob_client.upload_blob(
                    data=SpacesDir().model_dump_json(indent=2),
                    overwrite=False
                )
            else:
                raise Exception(f"Spaces directory already exists with _info.json")
        except Exception as e:
            raise Exception(f"Failed to create spaces directory: {str(e)}")

    async def _add_spaces_dir_info(self, space: Space) -> None:
        """Update the spaces directory info with new space info"""
        try:
            spaces_blob_client = self._space_container_client.get_blob_client(
                blob="spaces/_info.json"
            )
            if await spaces_blob_client.exists():
                # get existing spaces dir data
                stream = await spaces_blob_client.download_blob()
                spaces_blob_data = await stream.readall()
                spaces_dir = SpacesDir.model_validate_json(spaces_blob_data)

                # update spaces dir with space base info
                space_base = SpaceBase(
                    space_id=space.space_id,
                    name=space.name,
                )
                spaces_dir.spaces.append(space_base)

                # upload updated spaces dir data and overwrite
                await spaces_blob_client.upload_blob(
                    spaces_dir.model_dump_json(),
                    overwrite=True,
                )
            else:
                raise Exception(f"Spaces directory does not exist with _info.json")
        except Exception as e:
            raise Exception(f"Failed to update spaces directory: {str(e)}")

    async def _delete_spaces_dir_info(self, space_name: str) -> None:
        """Delete a space from the spaces directory info using space name"""
        try:
            spaces_blob_client = self._space_container_client.get_blob_client(
                blob="spaces/_info.json"
            )
            if await spaces_blob_client.exists():
                # get existing spaces dir data
                stream = await spaces_blob_client.download_blob()
                spaces_blob_data = await stream.readall()
                spaces_dir = SpacesDir.model_validate_json(spaces_blob_data)

                # delete space from spaces dir
                spaces_dir.spaces = [s for s in spaces_dir.spaces if s.name != space_name]

                # upload updated spaces dir data and overwrite
                await spaces_blob_client.upload_blob(
                    spaces_dir.model_dump_json(),
                    overwrite=True,
                )
            ## NOTE: nothing to do if spaces dir does not exist
            # else:
            #     raise Exception(f"Spaces directory does not exist with _info.json")
        except Exception as e:
            raise Exception(f"Failed to delete space from spaces directory: {str(e)}")

    @staticmethod
    def _space_info_blob_name(space_name: str) -> str:
        """Get the blob name for space info"""
        return f"spaces/{space_name}/_info.json"

    async def create_space_info(self, space: Space) -> Space:
        """
        Create a new space with space info

        **Dependencies:**
        - self._async_init
        - self._space_info_blob_name
        - self._add_spaces_dir_info

        Args:
            space: The space object to create

        Returns:
            Space: The created space object

        Raises:
            Exception: If there's an error during the creation process
        """
        try:
            self.logger.info(f"Creating new space with name: {space.name}")
            await self._async_init()

            space_blob_client = self._space_container_client.get_blob_client(
                blob=self._space_info_blob_name(space.name)
            )

            if await space_blob_client.exists():
                self.logger.warning(f"Space with name '{space.name}' already exists")
                raise SpaceAlreadyExistsError(f"Space with name '{space.name}' already exists")

            self.logger.debug("Adding space to spaces directory info")
            await self._add_spaces_dir_info(space)
            
            self.logger.debug("Uploading space info blob")
            await space_blob_client.upload_blob(
                data=space.model_dump_json(indent=2),
                overwrite=False
            )
            
            self.logger.info(f"Successfully created space: {space.name}")
            return space
        except SpaceError as e:
            self.logger.error(f"Space error while creating space '{space.name}': {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while creating space '{space.name}': {str(e)}")
            raise SpaceError(f"Failed to create space: {str(e)}")

    async def space_exists(self, space_name: str) -> bool:
        """
        Check if a space exists

        **Dependencies:**
        - self._space_info_blob_name

        Args:
            space_name: The name of the space to check

        Returns:
            bool: True if the space exists, False otherwise
        """
        try:
            # ensure async init is done
            await self._async_init()

            self.logger.debug(f"Checking if space '{space_name}' exists")
            space_blob_client = self._space_container_client.get_blob_client(
                blob=self._space_info_blob_name(space_name)
            )
            return await space_blob_client.exists()
        except Exception as e:
            self.logger.error(f"Failed to check if space exists: {str(e)}")
            raise Exception(f"Failed to check if space exists: {str(e)}")

    async def get_space_by_name(self, space_name: str) -> Space:
        """
        Get a space info by name

        **Dependencies:**
        - self._space_info_blob_name

        Args:
            space_name: The name of the space to retrieve

        Returns:
            Space: The retrieved space object

        Raises:
            Exception: If there's an error during the retrieval process
        """
        try:
            self.logger.info(f"Retrieving space with name: {space_name}")
            await self._async_init()

            space_blob_client = self._space_container_client.get_blob_client(
                blob=self._space_info_blob_name(space_name)
            )
            
            if not await space_blob_client.exists():
                self.logger.warning(f"Space '{space_name}' not found")
                raise SpaceNotFoundError(f"Space '{space_name}' not found")

            self.logger.debug(f"Downloading space data for: {space_name}")
            stream = await space_blob_client.download_blob()
            space_blob_data = await stream.readall()
            space = Space.model_validate_json(space_blob_data)
            
            self.logger.info(f"Successfully retrieved space: {space_name}")
            return space
        except SpaceError as e:
            self.logger.error(f"Space error while retrieving space '{space_name}': {str(e)}")
            raise
        except Exception as e:
            self.logger.error(f"Unexpected error while retrieving space '{space_name}': {str(e)}")
            raise SpaceError(f"Failed to retrieve space: {str(e)}")


    async def list_all_spaces_info(self) -> list[Space]:
        """
        List all spaces info

        **Dependencies:**
        - self.get_space_by_name

        Returns:
            list[Space]: List of all space objects

        Raises:
            Exception: If there's an error during the listing process
        """
        try:
            # ensure async init is done
            await self._async_init()

            spaces: list[Space] = []
            self.logger.info("Listing all spaces info")

            # async iterator
            space_blobs = self._space_container_client.walk_blobs(name_starts_with="spaces/", delimiter="/")
            async for blob in space_blobs:
                # get and validate space_name
                space_name = blob.name.split('/')[1]
                if space_name != "_info.json":
                    # get space info and append
                    space = await self.get_space_by_name(space_name)
                    spaces.append(space)
            return spaces
        except Exception as e:
            self.logger.error(f"Failed to list spaces: {str(e)}")
            raise Exception(f"Failed to list spaces: {str(e)}")

    async def delete_space_by_name(self, space_name: str) -> None:
        """
        Delete a space by name

        **Dependencies:**
        - self._space_info_blob_name
        - self._delete_spaces_dir_info

        Args:
            space_name: The name of the space to delete

        Note: This will delete space info and all files in the space.
        """
        try:
            self.logger.info(f"Deleting space with name: {space_name}")
            await self._async_init()

            space_blob_client = self._space_container_client.get_blob_client(
                blob=self._space_info_blob_name(space_name)
            )
            
            if not await space_blob_client.exists():
                self.logger.warning(f"Space '{space_name}' not found for deletion")
                return

            self.logger.debug(f"Removing space '{space_name}' from spaces directory")
            await self._delete_spaces_dir_info(space_name)

            self.logger.debug(f"Deleting space blob for '{space_name}'")
            await space_blob_client.delete_blob()

            self.logger.debug(f"Deleting all files in space '{space_name}'")
            space_blobs = self._space_container_client.list_blobs(
                name_starts_with=f"spaces/{space_name}/"
            )
            async for blob in space_blobs:
                blob_client = self._space_container_client.get_blob_client(blob=blob.name)
                await blob_client.delete_blob()

            self.logger.info(f"Successfully deleted space: {space_name}")
        except Exception as e:
            self.logger.error(f"Failed to delete space '{space_name}': {str(e)}")
            raise Exception(f"Failed to delete space: {str(e)}")
