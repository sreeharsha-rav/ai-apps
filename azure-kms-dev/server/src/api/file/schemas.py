from pydantic import BaseModel, Field
from typing import Optional, List

from .models import FileType, FileSource, FileProcessingStatus


class FileResponse(BaseModel):
    id: str = Field(
        ...,
        description="Unique identifier for the uploaded file",
        example="file_123e4567-e89b-12d3-a456-426614174000"
    )
    name: str = Field(
        ...,
        description="Original file name",
        example="example_file.pdf"
    )
    type: FileType = Field(
        ...,
        description="extension of the file (e.g., txt, pdf, docx)",
        example=FileType.PDF
    )
    size: int = Field(
        ...,
        description="File size in bytes",
        example=102400
    )
    source: FileSource = Field(
        ...,
        description="Source of the file (e.g., system, onedrive)",
        example=FileSource.SYSTEM
    )
    url: str = Field(
        ...,
        description="URL to access the uploaded file",
        example="https://azureblobstorage.com/user_uploads/temp/file_123e4567-e89b-12d3-a456-426614174000/example_file.pdf"
    )
    extracted_content_url: Optional[str] = Field(
        None,
        description="URL to access the extracted content of the file, if available",
        example="https://azureblobstorage.com/threads/thread_12345/extracted/file_12345.json"
    )
    processing_status: FileProcessingStatus = Field(
        ...,
        description="Current processing status of the file",
        example=FileProcessingStatus.PENDING
    )
    uploaded_at: str = Field(
        ...,
        description="Timestamp when the file was uploaded",
        example="2023-10-01T12:00:00Z"
    )

class MultipleFileResponse(BaseModel):
    files: List[FileResponse] = Field(
        ...,
        description="List of uploaded files",
        example=[]
    )
    total_count: int = Field(
        ...,
        description="Total number of files uploaded",
        example=3
    )
    success_count: int = Field(
        ...,
        description="Number of files successfully uploaded",
        example=2
    )
    failed_files: List[str] = Field(
        default_factory=list,
        description="List of filenames that failed to upload",
        example=["corrupted_file.pdf"]
    )
