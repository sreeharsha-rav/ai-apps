from azure.storage.blob.aio import ContainerClient
from typing import Optional, BinaryIO
from pathlib import Path
import aiofiles
import tempfile

from src.config.settings import get_storage_settings
from src.core.document_processor import Document
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

    async def upload_file_stream_to_blob(self, blob_name: str, file_stream: BinaryIO, metadata: Optional[dict[str, str]] = None) -> str:
        """
        Uploads a file stream to Azure Blob Storage.

        Args:
            blob_name: Path to the blob
            file_stream: File stream to upload
            metadata: Optional metadata to store with the blob

        Returns:
            str: URL of the uploaded blob
        """
        try:
            blob_client = await self._blob_container_client.upload_blob(
                name=blob_name,
                data=file_stream,
                blob_type="BlockBlob",
                overwrite=True,
                metadata=metadata
            )
            logger.info(f"Successfully uploaded file to blob storage: {blob_name}")
            return blob_client.url
        except Exception as e:
            logger.error(f"Failed to upload file to blob storage: {e}")
            raise RuntimeError(f"Failed to upload file to blob storage: {e}")

    async def upload_document_to_blob(self, blob_name: str, document: Document, metadata: Optional[dict[str, str]] = None) -> str:
        """
        Uploads a document to Azure Blob Storage.

        Args:
            blob_name: Path to the blob
            document: Document object containing name and content
            metadata: Optional metadata to store with the blob

        Returns:
            str: URL of the uploaded blob
        """
        try:
            blob_client = await self._blob_container_client.upload_blob(
                name=blob_name,
                data=document.model_dump_json(indent=2).encode('utf-8'),
                blob_type="BlockBlob",
                overwrite=True,
                metadata=metadata
            )
            logger.info(f"Successfully uploaded document '{document.id}' to blob storage: {blob_name}")
            return blob_client.url
        except Exception as e:
            logger.error(f"Failed to upload document to blob storage: {e}")
            raise RuntimeError(f"Failed to upload document to blob storage: {e}") from e

    async def download_blob_to_temp_file(self, blob_name: str) -> Path:
        """
        Downloads a blob to a temporary file.

        Args:
            blob_name: Path to the blob

        Returns:
            Path: Path to the temporary file
        """
        temp_path = None
        try:
            temp_file = tempfile.NamedTemporaryFile(delete=False)
            temp_path = Path(temp_file.name)
            temp_file.close()

            download_stream = await self._blob_container_client.download_blob(blob=blob_name)
            async with aiofiles.open(temp_path, 'wb') as f:
                async for chunk in download_stream.chunks():
                    await f.write(chunk)

            logger.info(f"Downloaded blob '{blob_name}' to temporary file '{temp_path}'")
            return temp_path
        except Exception as e:
            logger.error(f"Failed to download blob '{blob_name}' to temporary file: {e}")
            if temp_path and temp_path.exists():
                temp_path.unlink(missing_ok=True)
            raise RuntimeError(f"Failed to download blob '{blob_name}' to temporary file: {e}") from e