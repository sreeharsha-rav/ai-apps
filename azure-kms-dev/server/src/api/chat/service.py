import time
from uuid import uuid4
from typing import Optional
from fastapi import UploadFile

from .models import File, FileProcessingStatus
from .repository import FileRepository
from .utils import validate_filename, validate_file_size
from src.core.document_processor import DocumentProcessorFactory
from src.middleware.logging import logger


class ChatService:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    async def upload_file_stream(self, file: UploadFile) -> File:
        """
        Upload a file asynchronously.

        Args:
            file (UploadFile):

        Returns:
            File: An instance of the File model containing file details
        """
        try:
            # validate file
            filename, extension = validate_filename(filename=file.filename)
            size = await validate_file_size(upload_file=file)

            # generate blob name
            file_id = f"file_{uuid4()}"
            blob_name = f"temp/{file_id}/{filename}"

            logger.info(f"Uploading file: {file_id}, name: {filename}, size: {size} bytes, extension: {extension}")
            blob_url = await self.file_repository.upload_file_stream_to_blob(
                blob_name=blob_name,
                file=file
            )

            file = File(
                id=file_id,
                name=filename,
                extension=extension,
                size=size,  # size is already validated
                url=blob_url,
                extracted_content_url=None,     # yet to be processed
                processing_status=FileProcessingStatus.PENDING
            )
            logger.info(f"File upload completed: {file_id}")
            return file
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"File upload failed: {str(e)}")
            raise RuntimeError(f"Failed to process file upload: {str(e)}") from e

    async def process_file_background(self, file: File) -> Optional[File]:
        """
        Process the uploaded file (e.g., save to database, trigger background tasks).

        Args:
            file (File): The file to process.

        Returns:
            File: An instance of the File model containing processed file details.
        """
        start_time = time.time()
        temp_file_path = None
        try:
            logger.info(f"Starting background processing for file: {file.id}")
            file.processing_status = FileProcessingStatus.PROCESSING
            logger.info(f"File {file.id} status updated to {file.processing_status.value}")

            # download file to a temp file
            download_start = time.time()
            blob_name = f"temp/{file.id}/{file.name}"
            temp_file_path = await self.file_repository.download_blob_to_temp_file(blob_name)
            donwload_time = (time.time() - download_start) * 1000
            logger.info(f"Downloaded file {file.id} to temporary path: {temp_file_path}, time taken: {donwload_time:.2f} ms")

            # extract text from the file using the appropriate processor
            logger.info(f"Processing file: {file.id}, name: {file.name}, extension: {file.extension}")
            extract_start = time.time()
            processor = DocumentProcessorFactory.get_processor(file.extension)
            document = await processor.extract_text(temp_file_path=temp_file_path)
            extract_time = (time.time() - extract_start) * 1000
            logger.info(f"Extracted content from file: {file.id}, name: {file.name} into document: {document.id} in {extract_time:.2f} ms")

            # upload extracted content to blob storage
            upload_start = time.time()
            extracted_content_blob_name = f"files/{file.id}/extracted/{file.name}"
            extracted_content_url = await self.file_repository.upload_document_to_blob(
                blob_name=extracted_content_blob_name,
                document=document
            )
            upload_time = (time.time() - upload_start) * 1000
            logger.info(f"Uploaded extracted content for file {file.id} in {upload_time:.2f} ms")

            # create processed file object
            processed_file = File(
                id=file.id,
                name=file.name,
                extension=file.extension,
                size=file.size,
                url=file.url,  # original file URL
                extracted_content_url=extracted_content_url,
                processing_status=FileProcessingStatus.COMPLETED
            )
            logger.info(f"File {file.id} status updated to {processed_file.processing_status.value}")

            total_time = (time.time() - start_time) * 1000
            logger.info(f"Successfully processed file: {file.id} in {total_time:.2f} ms")

            return processed_file
        except Exception as e:
            total_time = (time.time() - start_time) * 1000
            logger.error(f"Error processing file: {str(e)} after {total_time:.2f} ms")
            if file:
                file.processing_status = FileProcessingStatus.FAILED
                logger.info(f"File {file.id} status updated to {file.processing_status.value}")
                # FUTURE: save the file status to the database
            else:
                logger.error("File object is None, cannot update processing status.")
            raise RuntimeError(f"Failed to process file: {str(e)}") from e
        finally:
            # clean up temp file if it exists
            if temp_file_path and temp_file_path.exists():
                try:
                    temp_file_path.unlink()
                    logger.debug(f"Temporary file {temp_file_path} deleted successfully.")
                except Exception as cleanup_error:
                    logger.warning(f"Failed to delete temporary file {temp_file_path}: {cleanup_error}")

