from pydantic import BaseModel, Field, ConfigDict
from ulid import ULID
from typing import Optional
from datetime import datetime

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
