import re
from typing import Optional, Tuple
from fastapi import UploadFile

from .constants import FILENAME_PATTERN, MAX_FILE_SIZE, READ_CHUNK_SIZE
from .models import FileType


def validate_filename(filename: str) -> Tuple[str, FileType]:
    """Validates the filename with a specific pattern and checks the file extension."""
    if not filename or not filename.strip():
        raise ValueError("Filename cannot be empty or whitespace.")

    if not re.match(FILENAME_PATTERN, filename):
        raise ValueError(f"Invalid file name: {filename}. Must match pattern: {FILENAME_PATTERN}")

    extension = filename.split('.')[-1].lower()
    valid_extensions = {ext.value for ext in FileType}
    if extension not in valid_extensions:
        raise ValueError(f"Invalid file type: {extension}. Supported types are: {', '.join(valid_extensions)}")

    # FUTURE: validate filename length based on storage system limits
    return filename, FileType(extension)

async def validate_file_size(upload_file: UploadFile) -> Optional[int]:
    """Validates the file size asynchronously in chunks."""
    total_size = 0
    while chunk := await upload_file.read(READ_CHUNK_SIZE):
        total_size += len(chunk)
        if total_size > MAX_FILE_SIZE:
            raise ValueError(f"File size exceeds the maximum limit of {MAX_FILE_SIZE} bytes. Provided size: {total_size} bytes.")

    await upload_file.seek(0)  # Reset the file pointer after reading
    return total_size