from typing import List
from uuid import UUID
from fastapi import UploadFile
from src.models.file import File, FileExtension
from src.repositories.space.file_repository import SpaceFileRepository
from src.core.exceptions.space import SpaceError
from src.schemas.file import FileUploadRequest, FileResponse
from s

class FileService:
    """Service for managing files within spaces"""

    def __init__(self):
        self._file_repository = SpaceFileRepository()

    def _get_file_extension(self, filename: str) -> FileExtension:
        """Extract and validate file extension"""
        ext = "." + filename.split(".")[-1].lower()
        try:
            return FileExtension(ext)
        except ValueError:
            raise SpaceError(f"Unsupported file extension: {ext}")

    async def upload_file(self, space_name: str, file_data: FileUploadRequest, upload_file: UploadFile) -> FileResponse:
        """Upload a file to a space"""
        try:
            # Validate file extension
            extension = self._get_file_extension(upload_file.filename)
            
            # Create file model
            file = File(
                base_name=file_data.base_name,
                extension=extension
            )
            
            # Read file content
            content = await upload_file.read()
            
            # Upload to storage
            uploaded_file = await self._file_repository.upload_file(space_name, file, content)
            
            # Create response
            return FileResponse(
                **uploaded_file.model_dump(),
                space_name=space_name,
                size_bytes=len(content)
            )
        except SpaceError:
            raise
        except Exception as e:
            raise SpaceError(f"Failed to upload file: {str(e)}")

    async def get_file(self, space_name: str, file_id: UUID) -> FileResponse:
        """Get file metadata"""
        file = await self._file_repository.get_file(space_name, file_id)
        content = await self._file_repository.download_file(space_name, file)
        return FileResponse(
            **file.model_dump(),
            space_name=space_name,
            size_bytes=len(content)
        )

    async def list_files(self, space_name: str) -> List[FileResponse]:
        """List all files in a space"""
        files = await self._file_repository.list_files(space_name)
        return [
            FileResponse(
                **file.model_dump(),
                space_name=space_name,
                size_bytes=0  # You might want to get actual sizes if needed
            )
            for file in files
        ]