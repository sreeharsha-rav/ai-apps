from uuid import uuid4
from fastapi import UploadFile

from .models import File
from .repository import FileRepository
from .utils import validate_filename, validate_file_size
from src.middleware.logging import logger


class ChatService:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    async def upload_file_and_process_stream(self, file: UploadFile):
        """
        Upload and process a file asynchronously in background.

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

            logger.info(f"Processing file upload: {filename} ({size} bytes)")

            blob_url = await self.file_repository.upload_file_stream_to_blob(
                blob_name=blob_name,
                file=file
            )

            file = File(
                id=file_id,
                filename=filename,
                type=extension,
                size=size,
                url=blob_url
            )
            logger.info(f"File upload completed: {file_id}")
            return file
        except ValueError:
            raise
        except Exception as e:
            logger.error(f"File upload failed: {str(e)}")
            raise RuntimeError(f"Failed to process file upload: {str(e)}") from e

