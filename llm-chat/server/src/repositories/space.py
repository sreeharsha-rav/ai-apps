from src.models.space import SpaceBase, Space, SpacesDir
from src.core.config import storage_settings
from azure.storage.blob.aio import ContainerClient
from src.utils.decorators import singleton

@singleton
class SpaceRepository:
    """Repository for managing spaces in storage"""

    def __init__(self):
        """Initialize the SpaceRepository"""
        try:
            self._space_container_client = ContainerClient.from_connection_string(
                conn_str=storage_settings.AZURE_STORAGE_CONNECTION_STRING,
                container_name=storage_settings.SPACE_CONTAINER_NAME
            )
            # # check if container exists, TODO: fix warning by add await
            # if not self._space_container_client.exists():
            #     raise Exception(f"Container \"{storage_settings.SPACE_CONTAINER_NAME}\" does not exist")
        except Exception as e:
            raise Exception(f"Failed to initialize SpaceRepository Azure Blob Storage client: {str(e)}")

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
            space_blob_client = self._space_container_client.get_blob_client(
                blob=self._space_info_blob_name(space.name)
            )

            if await space_blob_client.exists():
                raise Exception(f"Space with name \"{space.name}\" already exists, overwrite is not allowed")

            # update spaces dir info
            await self._add_spaces_dir_info(space)

            # upload space info
            await space_blob_client.upload_blob(
                data=space.model_dump_json(indent=2),
                overwrite=False
            )
            return space
        except Exception as e:
            raise Exception(f"Failed to create space: {str(e)}")

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
            space_blob_client = self._space_container_client.get_blob_client(
                blob=self._space_info_blob_name(space_name)
            )
            return await space_blob_client.exists()
        except Exception as e:
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
            space_blob_client = self._space_container_client.get_blob_client(
                blob=self._space_info_blob_name(space_name)
            )
            if await space_blob_client.exists():
                stream = await space_blob_client.download_blob()
                space_blob_data = await stream.readall()
                space = Space.model_validate_json(space_blob_data)
                return space
            else:
                raise Exception(f"Space with name \"{space_name}\" not found")
        except Exception as e:
            raise Exception(f"Failed to retrieve space: {str(e)}")


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
            spaces: list[Space] = []

            # async iterator
            space_blobs = self._space_container_client.list_blobs(name_starts_with="spaces/")
            async for blob in space_blobs:
                # only consider JSON files
                if blob.name.endswith('/_info.json'):
                    # get and validate space_name
                    space_name = blob.name.split('/')[1]
                    # get space info and append
                    space = await self.get_space_by_name(space_name)
                    spaces.append(space)
            return spaces
        except Exception as e:
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
            space_blob_name = self._space_info_blob_name(space_name)
            space_blob_client = self._space_container_client.get_blob_client(
                blob=space_blob_name
            )
            if not await space_blob_client.exists():
                return

            # delete space ifo from spaces dir info
            await self._delete_spaces_dir_info(space_name)

            # delete space info in space_name dir
            await space_blob_client.delete_blob()

            # delete all files in the space if any
            space_blobs = self._space_container_client.list_blobs(name_starts_with=f"spaces/{space_name}/")
            await self._space_container_client.delete_blobs(*space_blobs)
        except Exception as e:
            raise Exception(f"Failed to delete space: {str(e)}")
