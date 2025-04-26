from azure.storage.blob.aio import ContainerClient
from src.core.config import storage_settings
from src.utils.loggers import setup_logger

class BaseAzureBlobRepository:
    """Base repository for Azure Blob Storage operations"""
    
    def __init__(self, container_name: str):
        self.logger = setup_logger(name=f"{container_name}_repository")
        self._container_client = ContainerClient.from_connection_string(
            conn_str=storage_settings.AZURE_STORAGE_CONNECTION_STRING,
            container_name=container_name
        )
        self._initialized = False

    async def _ensure_initialized(self) -> None:
        """Ensure the repository is initialized"""
        if self._initialized:
            return

        try:
            exists = await self._container_client.exists()
            if not exists:
                self.logger.error(f"Container '{self._container_client.container_name}' does not exist")
                raise Exception(f"Container '{self._container_client.container_name}' does not exist")
            self._initialized = True
        except Exception as e:
            raise Exception(f"Failed to initialize repository: {str(e)}")

    async def _upload_json(self, blob_name: str, data: str, overwrite: bool = False) -> None:
        """Upload JSON data to a blob"""
        try:
            blob_client = self._container_client.get_blob_client(blob=blob_name)
            await blob_client.upload_blob(data=data, overwrite=overwrite)
        except Exception as e:
            raise Exception(f"Failed to upload blob '{blob_name}': {str(e)}")

    async def _download_json(self, blob_name: str):
        """Download JSON data from a blob"""
        try:
            blob_client = self._container_client.get_blob_client(blob=blob_name)
            stream = await blob_client.download_blob()
            return await stream.readall()
        except Exception as e:
            raise Exception(f"Failed to download blob '{blob_name}': {str(e)}")

    async def _delete_blob(self, blob_name: str) -> None:
        """Delete a blob"""
        try:
            blob_client = self._container_client.get_blob_client(blob=blob_name)
            await blob_client.delete_blob()
        except Exception as e:
            raise Exception(f"Failed to delete blob '{blob_name}': {str(e)}")

    async def _blob_exists(self, blob_name: str) -> bool:
        """Check if a blob exists"""
        try:
            blob_client = self._container_client.get_blob_client(blob=blob_name)
            return await blob_client.exists()
        except Exception as e:
            raise Exception(f"Failed to check blob existence '{blob_name}': {str(e)}")