from pydantic import BaseModel, Field
from enum import Enum
from typing import Literal
from uuid import uuid4
from datetime import datetime


class Role(str, Enum):
    USER = "user"
    SYSTEM = "system"
    ASSISTANT = "assistant"

class Message(BaseModel):
    role: Role = Field(
        ...,
        description="Role of the message sender (user, system, assistant)"
    )
    content: str = Field(
        min_length=1,
        pattern=r'\S+',
        description="Content of the message"
    )

class SystemMessage(Message):
    role: Literal[Role.SYSTEM] = Role.SYSTEM

class UserMessage(Message):
    role: Literal[Role.USER] = Role.USER

class AssistantMessage(Message):
    role: Literal[Role.ASSISTANT] = Role.ASSISTANT

class Chat(BaseModel):
    id: str = Field(
        default_factory=lambda: f"chat_{uuid4()}",
        min_length=41,
        max_length=41,
        pattern=r"^chat_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        description="Unique identifier for the chat"
    )
    messages: list[Message] = Field(
        ...,
        description="List of messages in the chat"
    )
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp when the chat was created"
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp when the chat was last updated"
    )
    