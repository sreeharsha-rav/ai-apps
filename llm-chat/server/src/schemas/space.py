from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional
from src.models.space import Space
from src.models.file import File
from ulid import ULID

RESERVED_SPACE_NAMES = {
    "spaces",
    "_info",
    "_info.json",
}

class SpaceRequest(BaseModel):
    """Request body for space endpoint"""
    name: str = Field(
        min_length=1,
        max_length=100,
        pattern=r'^[a-zA-Z0-9_\- ]+$',
        description="Name of the space"
    )
    description: Optional[str] = Field(
        description="Description of the space"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra = {
            "example": {
                "name": "Demo Space",
                "description": "This is a description of the demo space.",
            }
        },
        validate_default=True,
        frozen=True
    )

    @field_validator('name')
    @classmethod
    def validate_name_not_reserved(cls, v: str) -> str:
        if v.lower() in RESERVED_SPACE_NAMES:
            raise ValueError(f"Name '{v}' is reserved")
        return v

class SpaceResponse(Space):
    """Response body for space endpoint"""
    files: list[File] = Field(
        default=[],
        description="List of files in the space"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra = {
            "example": {
                "space_id": "01HQ8RDZQ24YBGN7PB9XQJM8JD",
                "name": "Demo Space",
                "description": "This is a description of the demo space.",
                "files": [
                    {
                        "file_id": "01HQ8RDZQ24YBGN7PB9XQJM8JD",
                        "base_name": "demo_file",
                        "extension": "txt",
                        "created_at": "2023-09-10T12:00:00",
                        "updated_at": "2023-09-10T12:00:00",
                    }
                ],
                "created_at": "2023-09-10T12:00:00",
                "updated_at": "2023-09-10T12:00:00",
            }
        },
        validate_default=True,
        frozen=True
    )