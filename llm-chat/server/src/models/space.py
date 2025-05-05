from pydantic import BaseModel, Field, ConfigDict
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

class Space(BaseModel):
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
    last_indexed: Optional[str] = Field(
        default="",
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
