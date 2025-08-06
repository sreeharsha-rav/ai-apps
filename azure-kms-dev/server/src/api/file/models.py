from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional
from datetime import datetime

from .constants import FILENAME_PATTERN


class FileSource(str, Enum):
    SYSTEM = "system"
    ONEDRIVE = "onedrive"

class FileType(str, Enum):
    TXT = "txt"
    PDF = "pdf"
    DOCX = "docx"

class FileProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class File(BaseModel):
    id: str = Field(
        ...,
        description="Unique identifier for the file"
    )
    name: str = Field(
        ...,
        pattern=FILENAME_PATTERN,
        description="Original file name"
    )
    type: FileType = Field(
        ...,
        description="Type of the file (e.g., txt, pdf, docx)"
    )
    size: int = Field(
        ...,
        description="File size in bytes"
    )
    source: FileSource = Field(
        ...,
        description="Source of the file (e.g., system, onedrive)"
    )
    url: Optional[str] = Field(
        None,
        description="Blob Storage URL for the file"
    )
    extracted_content_url: Optional[str] = Field(
        None,
        description="URL for the extracted content of the file, if applicable"
    )
    processing_status: FileProcessingStatus = Field(
        default=FileProcessingStatus.PENDING,
        description="Current processing status of the file"
    )
    uploaded_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Upload timestamp"
    )