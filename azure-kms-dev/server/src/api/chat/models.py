from pydantic import BaseModel, Field
from enum import Enum
from typing import Literal, Optional
from uuid import uuid4
from datetime import datetime

from .constants import FILENAME_PATTERN


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

class FileExtension(str, Enum):
    TXT = "txt"
    PDF = "pdf"
    DOCX = "docx"

class FileProcessingStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class File(BaseModel):
    id: str = Field(
        default_factory=lambda: f"file_{uuid4()}",
        max_length=41,
        min_length=41,
        pattern=r"^file_[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$",
        description="Unique identifier for the file"
    )
    name: str = Field(
        ...,
        pattern=FILENAME_PATTERN,
        description="Original file name"
    )
    extension: FileExtension = Field(
        ...,
        description="Extension of the file (e.g., txt, pdf, docx)"
    )
    size: int = Field(
        ...,
        description="File size in bytes"
    )
    uploaded_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Upload timestamp"
    )
    url: Optional[str] = Field(
        None,
        description="Blob Storage URL for the file"
    )
    extracted_content_url: Optional[str] = Field(
        None,
        description="URL for the extracted content of the file, if applicable"
    )
    processing_status: FileProcessingStatus = Field(
        default=FileProcessingStatus.PENDING,
        description="Current processing status of the file"
    )