from enum import Enum
from pydantic import BaseModel, Field, ConfigDict
from ulid import ULID
from datetime import datetime

class FileExtension(str, Enum):
    """Enum for allowed file extensions"""
    TXT = "txt"
    PDF = "pdf"
    DOCX = "docx"
    DOC = "doc"
    # add more as needed

class FileBase(BaseModel):
    """Base file model with core fields"""
    file_id: ULID = Field(
        default_factory=ULID,
        description="Unique file identifier"
    )
    base_name: str = Field(
        min_length=1,
        max_length=200,                           # NOTE: max azure blob name from root dir is 1024
        pattern="^[a-zA-Z0-9_\- ]+$",             # allowed file names pattern
        description="File name without extension"
    )
    extension: FileExtension = Field(
        description="File type extension"
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra = {
            "example": {
                "id": "01HQ8RDZQ24YBGN7PB9XQJM8JD",
                "base_name": "example_file",
                "extension": "txt",
            }
        },
        validate_default=True,
        frozen=True,
    )

class File(FileBase):
    """Extended file model with timestamps"""
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        description="Last update timestamp"
    )