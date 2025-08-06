import time
from uuid import uuid4
from io import BytesIO
from typing import Dict, Optional, BinaryIO

from .models import File, FileProcessingStatus, FileSource, FileType
from .repository import FileRepository
from src.core.document_processor import DocumentProcessorFactory
from src.middleware.logging import logger


class FileService:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository
        self._file_cache: Dict[str, File] = {}         # in-memory cache for file status (FUTURE: replace with database)

    def get_file_metadata(self, file_id: str) -> Optional[File]:
        """
        Get the metadata of a file by its ID.

        Args:
            file_id (str): The ID of the file to retrieve status for.

        Returns:
            Optional[File]: The File object if found, otherwise None.
        """
        file = self._file_cache.get(file_id)
        if file:
            logger.info(f"Retrieved file metadata from cache: {file_id}")
            return file
        else:
            logger.warning(f"File metadata not found in cache: {file_id}")

    def _update_file_status(self, file: File, processing_status: FileProcessingStatus) -> None:
        """
        Update the status of a file in the in-memory cache.

        Args:
            file (File): The File object with updated status.
        """
        file.processing_status = processing_status
        self._file_cache[file.id] = file
        # FUTURE: also update in database if implemented
        logger.info(f"File status updated: {file.id} - {processing_status.value}")

    async def upload_file_stream(self, source: FileSource, filename: str, file_type: FileType, size: int, file_stream: BinaryIO) -> File:
        """
        Upload a file asynchronously.

        Args:
            source (FileSource): Source of the file (e.g., system, onedrive)
            filename (str): Name of the file to upload
            file_type (FileType): Type of the file (e.g., pdf, docx)
            size (int): Size of the file in bytes
            file_stream (BinaryIO): Stream of the file to upload

        Returns:
            File: An instance of the File model containing file details
        """
        try:
            # generate blob name
            file_id = f"file_{uuid4()}"
            blob_name = f"temp/{file_id}/{filename}"

            logger.info(f"Uploading file: {file_id}, name: {filename}, size: {size} bytes, type: {type}")
            blob_url = await self.file_repository.upload_file_stream_to_blob(
                blob_name=blob_name,
                file_stream=file_stream
            )

            file = File(
                id=file_id,
                name=filename,
                type=file_type,  # type is already validated
                size=size,  # size is already validated
                source=source,
                url=blob_url,
                extracted_content_url=None,     # yet to be processed
                processing_status=FileProcessingStatus.PENDING
            )
            self._update_file_status(file, FileProcessingStatus.PENDING)        # store initial file status
            logger.info(f"File upload completed: {file_id}")
            return file
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"File upload failed: {str(e)}")
            raise RuntimeError(f"Failed to process file upload: {str(e)}") from e

    async def process_file_background(self, file: File, content: bytes) -> Optional[File]:
        """
        Process the uploaded file (e.g., save to database, trigger background tasks).

        Args:
            file (File): The file to process.
            content (bytes): The content of the file to process.

        Returns:
            File: An instance of the File model containing processed file details.
        """
        start_time = time.time()
        try:
            logger.info(f"Starting background processing for file: {file.id}, name: {file.name}, type: {file.type}, size: {file.size} bytes")
            file_bytes = BytesIO(content)
            self._update_file_status(file, FileProcessingStatus.PROCESSING)

            # extract text from the file using the appropriate processor
            extract_start = time.time()
            processor = DocumentProcessorFactory.get_processor(file.type)
            extracted_content = await processor.extract_text(filename=file.name, file_bytes=file_bytes)
            extract_time = (time.time() - extract_start) * 1000
            logger.info(f"Extracted content from file: {file.id}, name: {file.name} in {extract_time:.2f} ms")

            # upload extracted content to blob storage
            upload_start = time.time()
            extracted_content_blob_name = f"files/{file.id}/extracted/{file.name}"
            extracted_content_url = await self.file_repository.upload_content_to_blob(
                blob_name=extracted_content_blob_name,
                content=extracted_content
            )
            upload_time = (time.time() - upload_start) * 1000
            logger.info(f"Uploaded extracted content for file {file.id} in {upload_time:.2f} ms")

            # create processed file object
            processed_file = File(
                id=file.id,
                name=file.name,
                type=file.type,
                size=file.size,
                source=file.source,
                url=file.url,  # original file URL
                extracted_content_url=extracted_content_url,
                processing_status=FileProcessingStatus.COMPLETED
            )
            self._update_file_status(processed_file, FileProcessingStatus.COMPLETED)

            total_time = (time.time() - start_time) * 1000
            logger.info(f"Successfully processed file: {file.id} in {total_time:.2f} ms")

            return processed_file
        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            logger.error(f"Error processing file: {str(e)} after {total_time:.2f} ms")
            self._update_file_status(file, FileProcessingStatus.FAILED)
            raise RuntimeError(f"Failed to process file: {str(e)}") from e