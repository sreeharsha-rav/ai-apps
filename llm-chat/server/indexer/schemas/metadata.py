from pydantic import BaseModel, Field, ConfigDict, field_validator
from ulid import ULID
from typing import Optional
from datetime import datetime
from enum import Enum

class IndexingStatus(str, Enum):
    """Enum representing the status of indexing."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETE = "complete"
    # FAILED = "failed"             # TODO

class SpaceMetadata(BaseModel):
    """Model for a space metadata."""
    space_id: str = Field(
        default_factory=lambda: str(ULID()),
        description="Unique identifier for the space using ULID."
    )
    name: str = Field(
        min_length=1,
        max_length=100,
        pattern=r'^[a-zA-Z0-9_\- ]+$',
        description="Name of the space."
    )
    description: Optional[str] = Field(
        default="",
        min_length=0,
        max_length=256,
        description="Description of the space."
    )
    indexing_status: IndexingStatus = Field(
        default=IndexingStatus.PENDING,
        description="Indexing status of the space."
    )
    last_indexed: str = Field(
        default=None,
        description="Timestamp of the last indexing."
    )
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp when the space was created."
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp when the space was last updated."
    )

    model_config = ConfigDict(
        from_attributes=True
    )

FILE_EXTENSIONS = { "txt", "pdf", "docx", "doc" }

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
    extension: str = Field(
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

    @field_validator("extension")
    def validate_extension(cls, extension):
        """
        Validate file extension
        """
        if extension not in FILE_EXTENSIONS:
            raise ValueError(f"Invalid file extension. Allowed extensions: {FILE_EXTENSIONS}")
        return extension

    @property
    def get_file_name(self) -> str:
        """
        Get full file name with extension
        """
        return f"{self.base_name}.{self.extension}"