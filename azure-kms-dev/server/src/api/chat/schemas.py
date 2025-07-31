from pydantic import BaseModel, Field, field_validator, ConfigDict
from typing import Optional

from .models import Role, FileProcessingStatus


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

class FileUploadResponse(BaseModel):
    id: str = Field(
        ...,
        description="Unique identifier for the uploaded file",
        example="file_123e4567-e89b-12d3-a456-426614174000"
    )
    name: str = Field(
        ...,
        description="Original file name",
        example="example_file.pdf"
    )
    extension: str = Field(
        ...,
        description="extension of the file (e.g., txt, pdf, docx)",
        example="pdf"
    )
    size: int = Field(
        ...,
        description="File size in bytes",
        example=102400
    )
    uploaded_at: str = Field(
        ...,
        description="Timestamp when the file was uploaded",
        example="2023-10-01T12:00:00Z"
    )
    url: str = Field(
        ...,
        description="URL to access the uploaded file",
        example="https://azureblobstorage.com/user_uploads/temp/file_123e4567-e89b-12d3-a456-426614174000/example_file.pdf"
    )
    extracted_content_url: Optional[str] = Field(
        None,
        description="URL to access the extracted content of the file, if available",
        example="https://azureblobstorage.com/threads/thread_12345/extracted/file_12345.json"
    )
    processing_status: FileProcessingStatus = Field(
        ...,
        description="Current processing status of the file",
        example=FileProcessingStatus.PENDING
    )
