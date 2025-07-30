from azure.storage.blob.aio import ContainerClient
from typing import Optional
from fastapi import UploadFile

from src.config.settings import get_storage_settings
from src.middleware.logging import logger


storage_settings = get_storage_settings()

class FileRepository:
    """Repository for handling file attachments in chat threads."""

    def __init__(self):
        self._blob_container_client = ContainerClient.from_connection_string(
            conn_str=storage_settings.AZURE_STORAGE_CONNECTION_STRING,
            container_name=storage_settings.AZURE_STORAGE_CONTAINER_NAME
        )
        logger.info("Initialized FileRepository with Async Azure Blob Storage client.")

    async def upload_file_stream_to_blob(self, blob_name: str, file: UploadFile, metadata: Optional[dict[str, str]] = None) -> str:
        """
        Uploads a file stream to Azure Blob Storage.

        Args:
            blob_name: Path to the blob
            file: file stream
            metadata: Optional metadata to store with the blob

        Returns:
            str: URL of the uploaded blob
        """
        try:
            blob_client = await self._blob_container_client.upload_blob(
                name=blob_name,
                data=file.file,
                blob_type="BlockBlob",
                overwrite=True,
                metadata=metadata
            )
            logger.info(f"Successfully uploaded file to blob storage: {blob_name}")
            return blob_client.url
        except Exception as e:
            logger.error(f"Failed to upload file to blob storage: {e}")
            raise RuntimeError(f"Failed to upload file to blob storage: {e}")

    async def download_from_blob(self, blob_name: str) -> bytes:
        """
        Downloads a file from Azure Blob Storage.

        Args:
            blob_name: Path to the blob

        Returns:
            bytes: Content of the downloaded blob
        """
        try:
            blob_client = self._blob_container_client.get_blob_client(blob=blob_name)
            download_stream = await blob_client.download_blob()
            data = await download_stream.readall()
            logger.info(f"Successfully downloaded file from blob storage: {blob_name}")
            return data
        except Exception as e:
            logger.error(f"Failed to download file from blob storage: {e}")
            raise RuntimeError(f"Failed to download file from blob storage: {e}")
