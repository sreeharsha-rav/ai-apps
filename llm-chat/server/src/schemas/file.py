from pydantic import BaseModel, Field, field_validator, ConfigDict
from src.models.file import File, FileExtension

RESERVED_FILE_NAMES = {
    "files",
    "_info",
    "_metadata",
    "metadata",
}

class FileRequest(BaseModel):
    """Request body for file endpoint"""
    base_name: str = Field(
        min_length=1,
        max_length=100,
        pattern=r'^[a-zA-Z0-9_\- ]+$',
        description="Base name of the file without extension"
    )
    extension: FileExtension = Field(description="Extension of the file")

    @field_validator('base_name')
    @classmethod
    def validate_base_name_not_reserved(cls, v: str) -> str:
        if v.lower() in RESERVED_FILE_NAMES:
            raise ValueError(f"Name '{v}' is reserved")
        return v

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra={
            "example": {
                "base_name": "demo_file",
                "extension": "txt",
            }
        },
        validate_default=True,
        frozen=True,
    )

class FileResponse(File):
    """Response body for file endpoint"""
    # space_name: str = Field(description="Name of the space the file belongs to")
    # size_bytes: int = Field(description="Size of the file in bytes")

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra = {
            "example": {
                "file_id": "01HQ8RDZQ24YBGN7PB9XQJM8JD",
                "base_name": "demo_file",
                "extension": "txt",
                "created_at": "2023-09-10T12:00:00",
                "updated_at": "2023-09-10T12:00:00",
            }
        },
        validate_default=True,
        frozen=True,
    )