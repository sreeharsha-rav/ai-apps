from pydantic import BaseModel, Field, field_validator
from typing import Optional

from .models import Role


class ChatRequest(BaseModel):
    chat_id: Optional[str] = Field(
        None,
        min_length=41,
        max_length=41,
        pattern=r"^chat_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        description="The ID of the chat to retrieve or create",
        example="chat_123e4567-e89b-12d3-a456-426614174000"
    )
    role: Role = Field(
        default=Role.USER,
        description="Role of the user in the chat (e.g., 'user', 'assistant')",
        example=Role.USER
    )
    content: str = Field(
        min_length=1,
        pattern=r"\S+",
        description="Content of the chat message",
        example="What is Artificial Intelligence?"
    )

    @field_validator("role")
    def validate_role(cls, value: str) -> str:
        """Validate the role field."""
        if value not in [Role.USER, Role.ASSISTANT]:
            raise ValueError(f"Invalid role: {value}. Must be one of {Role.USER}, {Role.ASSISTANT}.")
        return value

class ChatResponse(BaseModel):
    chat_id: str = Field(
        ...,
        min_length=41,
        max_length=41,
        pattern=r"^chat_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        description="The ID of the chat",
        example="chat_123e4567-e89b-12d3-a456-426614174000"
    )
    role: Role = Field(
        ...,
        description="Role of the user in the chat (e.g., 'user', 'assistant')",
        example=Role.ASSISTANT
    )
    content: str = Field(
        ...,
        min_length=1,
        pattern=r"\S+",
        description="Content of the chat message",
        example="Artificial Intelligence is the simulation of human intelligence in machines."
    )
    created_at: str = Field(
        ...,
        description="Timestamp when the chat message was created",
        example="2023-10-01T12:00:00Z"
    )
