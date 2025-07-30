from pydantic import BaseModel, Field
from typing import Dict, Any, Optional
from uuid import uuid4
from datetime import datetime


class Document(BaseModel):
    """Schema for a document in the system."""

    id: str = Field(
        default_factory=lambda: f"doc_{uuid4()}",
        description="Unique identifier for the document"
    )
    name: str = Field(
        min_length=1,
        pattern=r'\S+',
        description="Original file name",
    )
    content: str = Field(
        min_length=1,
        pattern=r'\S+',
        description="Extracted content of the document",
    )
    size: Optional[int] = Field(
        default=None,
        ge=0,
        description="Size of the original file in bytes",
    )
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp when the document was created"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Additional metadata about the document"
    )