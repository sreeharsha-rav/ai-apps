from uuid import uuid4
import re

from .models import FileExtension, File
from .repository import FileRepository
from src.config.constants import MAX_FILE_SIZE
from src.middleware.logging import logger


class ChatService:
    def __init__(self, file_repository: FileRepository):
        self.file_repository = file_repository

    async def upload_file_and_process(self, file_extension: str, filename: str, content: bytes, size: int) -> File:
        """
        Upload and process a file asynchronously in background.

        Args:
            file_extension (str): The file extension/type of the file being uploaded
            filename (str): Name of the file being uploaded
            content (bytes): Content of the file being uploaded

        Returns:
            File: An instance of the File model containing file details
        """
        # validate file
        filename_pattern = r'^[a-zA-Z0-9_\-\[\]\(\)\{\} ]+\.[a-zA-Z]+$'
        if not re.match(filename_pattern, filename):
            raise ValueError(f"Invalid file name: {filename}.")

        valid_file_extensions = {ext.value for ext in FileExtension}
        if file_extension not in valid_file_extensions:
            raise ValueError(f"Invalid file type: {file_extension}. Supported types are: {', '.join(valid_file_extensions)}")

        if size > MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds the maximum limit of {MAX_FILE_SIZE} bytes. Provided size: {size} bytes.")

        try:
            file_id = f"file_{uuid4()}"
            blob_name = f"temp/{file_id}/{filename}"

            logger.info(f"Processing file upload: {filename} ({len(content)} bytes)")

            blob_url = await self.file_repository.upload_to_blob(
                blob_name=blob_name,
                content=content
            )

            file = File(
                id=file_id,
                filename=filename,
                type=FileExtension(file_extension),
                size=size,
                url=blob_url
            )
            logger.info(f"File upload completed: {file_id}")
            return file
        except ValueError as e:
            raise
        except Exception as e:
            logger.error(f"File upload failed for '{filename}': {str(e)}")
            raise RuntimeError(f"Failed to process file upload for '{filename}': {str(e)}") from e