from src.models.space import Space
from src.core.config import storage_settings
from src.utils.decorators import singleton
from .interfaces import ISpaceRepository
from azure.storage.blob.aio import ContainerClient, BlobClient
from src.utils.loggers import setup_logger
from typing import List

@singleton
class SpaceRepository(ISpaceRepository):
    """Repository for managing spaces in azure blob storage"""

    def __init__(self):
        self._space_container_client = ContainerClient.from_connection_string(
            conn_str=storage_settings.AZURE_STORAGE_CONNECTION_STRING,
            container_name=storage_settings.SPACE_CONTAINER_NAME
        )
        self.logger = setup_logger(name="space_repository")

    def _get_space_blob_client(self, space_name: str) -> BlobClient:
        """Get the blob name for space"""
        space_blob_name = f"spaces/{space_name}/_info.json"
        space_blob_client = self._space_container_client.get_blob_client(blob=space_blob_name)
        return space_blob_client

    async def space_exists(self, space_name: str) -> bool:
        """Check if a space exists"""
        self.logger.debug(f"Checking if space exists: {space_name}")
        space_blob_client = self._get_space_blob_client(space_name)
        exists = await space_blob_client.exists()
        self.logger.debug(f"Space '{space_name}' exists: {exists}")
        return exists

    async def create_new_space(self, space: Space) -> Space:
        """Create a new space with space info"""
        try:
            self.logger.info(f"Creating new space: {space.name}")
            space_blob_client = self._get_space_blob_client(space.name)
            self.logger.debug(f"Uploading space metadata for: {space.name}")
            await space_blob_client.upload_blob(
                data="b{}",
                metadata=space.model_dump(),
                overwrite=False
            )
            self.logger.info(f"Successfully created space: {space.name}")
            return space
        except Exception as e:
            self.logger.error(f"Failed to create space '{space.name}': {str(e)}")
            raise

    async def get_by_name(self, space_name: str) -> Space:
        """Get a space by name"""
        try:
            self.logger.info(f"Getting space by name: {space_name}")
            space_blob_client = self._get_space_blob_client(space_name)
            space_blob_properties = await space_blob_client.get_blob_properties()
            space_blob_metadata = space_blob_properties.metadata
            space = Space(**space_blob_metadata)
            self.logger.info(f"Successfully retrieved space: {space_name}")
            return space
        except Exception as e:
            self.logger.error(f"Failed to get space '{space_name}': {str(e)}")
            raise

    # async def get_by_id(self, space_id: str) -> Space:
    #     """Get a space by id"""
    #     try:
    #         self.logger.info(f"Getting space by id: {space_id}")
    #         space_blob_client = self._get_space_blob_client(space_id)
    #         space_blob_properties = await space_blob_client.get_blob_properties()
    #         space_blob_metadata = space_blob_properties.metadata
    #         space = Space(**space_blob_metadata)
    #         self.logger.info(f"Successfully retrieved space: {space_id}")
    #         return space
    #     except Exception as e:
    #         self.logger.error(f"Failed to get space '{space_id}': {str(e)}")
    #         raise

    async def list_all_spaces(self) -> List[Space]:
        """List all spaces"""
        try:
            self.logger.info("Listing all spaces")
            spaces = []
            processed_spaces = set()  # Track processed space names

            # List only _info.json files in spaces directory
            async for blob in self._space_container_client.list_blobs(name_starts_with="spaces/"):
                # Parse the blob name to get space name
                parts = blob.name.split("/")
                if len(parts) == 3 and parts[2] == "_info.json":
                    space_name = parts[1]
                    
                    # Skip if we've already processed this space
                    if space_name in processed_spaces:
                        self.logger.debug(f"Skipping duplicate space: {space_name}")
                        continue
                        
                    self.logger.debug(f"Processing space info for: {space_name}")
                    try:
                        # Get the space using existing method
                        space = await self.get_by_name(space_name)
                        spaces.append(space)
                        processed_spaces.add(space_name)
                    except Exception as e:
                        self.logger.warning(f"Failed to process space '{space_name}': {str(e)}")
                        continue

            self.logger.info(f"Successfully listed {len(spaces)} unique spaces")
            return spaces
        except Exception as e:
            self.logger.error(f"Failed to list spaces: {str(e)}")
            raise

    async def delete_by_name(self, space_name: str) -> None:
        """
        Delete a space by name

        Note: This will delete space info and all files in the space.
        """
        try:
            self.logger.info(f"Deleting space: {space_name}")
            space_blob_client = self._get_space_blob_client(space_name)
            await space_blob_client.delete_blob()

            # Delete all files in space
            self.logger.debug(f"Deleting all files in space: {space_name}")
            async for blob in self._space_container_client.walk_blobs(
                name_starts_with=f"spaces/{space_name}/files/"
            ):
                self.logger.debug(f"Deleting blob: {blob.name}")
                space_blob_client = self._space_container_client.get_blob_client(blob=blob.name)
                await space_blob_client.delete_blob()
            self.logger.info(f"Successfully deleted space: {space_name}")
        except Exception as e:
            self.logger.error(f"Failed to delete space '{space_name}': {str(e)}")
            raise
