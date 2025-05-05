from pydantic import BaseModel, Field, ConfigDict
from ulid import ULID

class RawDocument(BaseModel):
    """Represents a raw document blob from Azure Storage."""

    user_id: str
    space_name: str
    file_name: str
    file_extension: str         # TODO: validate extension
    blob_path: str
    content: bytes
    # content_type: Optional[str] = None    # Not required for current use case

    model_config = ConfigDict(
        arbitrary_types_allowed=True
    )

class ParsedDocument(BaseModel):
    """Represents a parsed document."""
    doc_id: str = Field(default_factory=lambda: str(ULID()))
    user_id: str
    space_name: str
    file_name: str
    blob_path: str
    content: str
    # content_type: Optional[str] = None    # Not required for current use case

class TextChunk(BaseModel):
    """Represents a text chunk."""
    chunk_id: str
    doc_id: str
    chunk_content: str
    chunk_index: int
    user_id: str
    space_name: str
    file_name: str
    blob_path: str

class VectorizedChunk(TextChunk):
    """Represents a vectorized text chunk."""
    chunk_vector: list[float]