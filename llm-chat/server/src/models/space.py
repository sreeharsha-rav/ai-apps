from pydantic import BaseModel, Field
from src.models.file import FileBase
from ulid import ULID
from typing import Optional
from datetime import datetime

class SpaceBase(BaseModel):
    """Base schema for a space info."""
    space_id: ULID = Field(
        default_factory=ULID,
        description="Unique identifier for the space using ULID."
    )
    name: str = Field(
        min_length=1,
        max_length=100,                 # NOTE: name of space should not exceed 1024 characters for azure blob
        pattern=r'^[a-zA-Z0-9_\- ]+$',  # NOTE: name of space should only contain alphanumeric characters, underscores, hyphens, and spaces
        description="Name of the space."
    )

class Space(SpaceBase):
    """Schema for a space info with additional metadata."""
    description: Optional[str] = Field(
        default="",
        min_length=0,
        max_length=256,
        description="Description of the space."
    )
    files: list[FileBase] = Field(
        default=[],
        description="List of files in the space."
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        description="Timestamp when the space was created."
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        description="Timestamp when the space was last updated."
    )

class SpacesDir(BaseModel):
    """Schema for spaces dir info with some optional metadata."""
    spaces: list[SpaceBase] = Field(
        default=[],
        description="List of spaces with base information."
    )
