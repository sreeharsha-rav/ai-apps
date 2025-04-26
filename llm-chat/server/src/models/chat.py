from datetime import datetime
from pydantic import BaseModel, Field
from ulid import ULID
from enum import Enum

class Role(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    DEVELOPER = "developer"
    SYSTEM = "system"

class Message(BaseModel):
    """Schema for a message in the chat application."""

    message_id: ULID = Field(
        default_factory=ULID,
        description="Unique identifier for the message using ULID."
    )
    role: Role = Field(
        description="The role of the message sender in the conversation."
    )
    content: str = Field(
        min_length=1,
        pattern=r'\S',  # Requires at least one non-whitespace character
        description="The content of the message."
    )

    model_config = {
        'str_strip_whitespace': True,
        "json_schema_extra": {
            "example": {
                "message_id": "01HQ8RDZQ24YBGN7PB9XQJM8JD",
                "role": "user",
                "content": "Hello, how are you?",
            }
        }
    }

class Chat(BaseModel):
    """Schema for a chat (conversation) in the application."""

    chat_id: ULID = Field(
        default_factory=ULID,
        description="Unique identifier for the chat using ULID."
    )
    title: str = Field(
        min_length=1,
        description="Title of the chat."
    )
    messages: list[Message] = Field(
        default_factory=list,
        description="List of messages in the chat."
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        description="Timestamp when the chat was created."
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(),
        description="Timestamp when the chat was last updated."
    )

    model_config = {
        'str_strip_whitespace': True,
        "json_schema_extra": {
            "example": {
                "chat_id": "01HQ8RDZQ24YBGN7PB9XQJM8JD",
                "title": "General Chat",
                "messages": [
                    {
                        "message_id": "01HQ8RDZQ24YBGN7PB9XQJM8JD",
                        "role": "user",
                        "content": "Hello, how are you?",
                    },
                    {
                        "message_id": "01HQ8RDZQ24YBGN7PB9XQJM8JD",
                        "role": "assistant",
                        "content": "I'm doing well, thank you!",
                    },
                ],
                "created_at": "2023-09-10T12:00:00",
                "updated_at": "2023-09-10T12:00:00",
            }
        }
    }