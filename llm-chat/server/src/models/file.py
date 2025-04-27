from pydantic import BaseModel, Field, ConfigDict
from ulid import ULID
from datetime import datetime
from enum import Enum

class FileExtension(str, Enum):
    """Enum for allowed file extensions"""
    TXT = "txt"
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    # add more as needed

class File(BaseModel):
    """File model for file metadata"""
    file_id: str = Field(
        default_factory=lambda: str(ULID()),
        description="Unique file identifier"
    )
    base_name: str = Field(
        min_length=1,
        max_length=200,  # NOTE: max azure blob name from root dir is 1024
        pattern=r'^[a-zA-Z0-9_\- ]+$',  # allowed file names pattern
        description="File name without extension"
    )
    extension: FileExtension = Field(
        description="File type extension"
    )
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Creation timestamp"
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Last update timestamp"
    )
