from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional
from src.models.space import Space

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
        str_strip_whitespace=True,
        json_schema_extra = {
            "example": {
                "name": "Demo Space",
                "description": "This is a description of the demo space.",
            }
        },
        validate_default=True,
        frozen=True,
    )

    @model_validator(mode='after')
    def validate_name_not_reserved(self) -> 'SpaceRequest':
        if self.name.lower() in RESERVED_SPACE_NAMES:
            raise ValueError(f"Name '{self.name}' is reserved")
        return self

class SpaceResponse(Space):
    """Response body for space endpoint"""

    # TODO: add required response fields here, not implemented yet

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra = {
            "example": {
                "space_id": "01HQ8RDZQ24YBGN7PB9XQJM8JD",
                "name": "Demo Space",
                "description": "This is a description of the demo space.",
                "created_at": "2023-09-10T12:00:00",
                "updated_at": "2023-09-10T12:00:00",
            }
        },
        validate_default=True,
        frozen=True,
    )