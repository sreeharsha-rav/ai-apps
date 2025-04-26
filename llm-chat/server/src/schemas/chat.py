from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Optional
from src.schemas.llm import ModelID
from src.models.chat import Message, Role
from ulid import ULID

class ChatMessageRequest(BaseModel):
    """Request body for chat endpoint"""
    
    chat_id: Optional[ULID] = Field(
        default_factory=ULID,
        description="The chat ULID to use for the chat completion"
    )
    message: Message = Field(
        default_factory=lambda: Message(role=Role.USER, content="hi"),
        description="The user message to send to the chat model"
    ) 
    model_id: ModelID = Field(
        default=ModelID.OPENAI_GPT4O_MINI,
        description="The model to use for the chat completion"
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra = {
            "example": {
                "chat_id": "01HQ8RDZQ24YBGN7PB9XQJM8JD",
                "message": {
                    "role": "user",
                    "content": "What are the latest advancements in AI?",
                },
                "model_id": "openai_gpt-4o-mini",
            }
        },
        validate_default=True,
        frozen=True,
    )

    @model_validator(mode='after')
    def validate_message_role(self) -> 'ChatMessageRequest':
        if self.message.role != Role.USER:
            raise ValueError("Message role must be 'user'")
        return self

class ChatMessageResponse(BaseModel):
    """Response body for chat endpoint"""
    
    chat_id: ULID = Field(
        description="The chat ULID"
    )
    message: Message = Field(
        default_factory=lambda: Message(role=Role.ASSISTANT, content="hello, I'm an AI assistant"),
        description="The assistant message returned by the chat model"
    )
    model_id: ModelID = Field(
        default=ModelID.OPENAI_GPT4O_MINI,
        description="The model used for the chat completion"
    )

    model_config = ConfigDict(
        str_strip_whitespace=True,
        json_schema_extra = {
            "example": {
                "chat_id": "01HQ8RDZQ24YBGN7PB9XQJM8JD",
                "message": {
                    "role": "assistant",
                    "content": "Latest advancements in AI include developments in natural language processing...",
                },
                "model_id": "openai_gpt-4o-mini",
            }
        },
        validate_default=True,
        frozen=True,
    )

    @model_validator(mode='after')
    def validate_message_role(self) -> 'ChatMessageResponse':
        if self.message.role != Role.ASSISTANT:
            raise ValueError("Message role must be 'assistant'")
        return self
