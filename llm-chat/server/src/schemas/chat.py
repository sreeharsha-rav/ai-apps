from datetime import datetime
from pydantic import BaseModel, Field, model_validator
from typing import Literal, Optional, List
from src.schemas.llm import ModelID
from enum import Enum
from ulid import ULID

from src.schemas.search import SearchResult


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
        'str_strip_whitespace': True,  # Automatically strip whitespace for all str fields
    }

class UserMessage(Message):
    """Schema for a user message in the chat application."""
    
    role: Literal[Role.USER] = Field(
        Role.USER,
        description="The role of the message sender in the conversation."
    )

class AssistantMessage(Message):
    """Schema for an assistant message in the chat application."""
    
    role: Literal[Role.ASSISTANT] = Field(
        Role.ASSISTANT,
        description="The role of the message sender in the conversation."
    )

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
    messages: List[Message] = Field(
        default_factory=list,
        description="List of messages in the chat."
    )
    created_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp when the chat was created."
    )
    updated_at: str = Field(
        default_factory=lambda: datetime.now().isoformat(),
        description="Timestamp when the chat was last updated."
    )

class ChatRequest(BaseModel):
    """Request body for chat endpoint"""
    
    chat_id: Optional[ULID] = Field(
        default_factory=ULID,
        description="The chat ULID to use for the chat completion"
    )
    message: UserMessage = Field(
        description="The user message to send to the chat model"
    ) 
    model_id: ModelID = Field(
        default=ModelID.OPENAI_GPT4O_MINI,
        description="The model to use for the chat completion"
    )

    class Config:
        """Configuration for ChatRequest model"""
        json_schema_extra = {
            "example": {
                "chat_id": "01HQ8RDZQ24YBGN7PB9XQJM8JD",
                "message": {
                    "role": "user",
                    "content": "What are the latest advancements in AI?",
                },
                "model_id": "openai_gpt-4o-mini",
            }
        }

class ChatResponse(BaseModel):
    """Response body for chat endpoint"""
    
    chat_id: ULID = Field(
        description="The chat ULID"
    )
    message: AssistantMessage = Field(
        description="The assistant message returned by the chat model"
    )
    model_id: ModelID = Field(
        default=ModelID.OPENAI_GPT4O_MINI,
        description="The model used for the chat completion"
    )
    # web_search: bool = Field(
    #     default=False,
    #     description="Indicates if a web search was performed"
    # )
    # search_results: Optional[List[SearchResult]] = Field(
    #     default=None,
    #     description="The search results returned by the web search"
    # )

    class Config:
        """Configuration for ChatResponse model"""
        json_schema_extra = {
            "example": {
                "chat_id": "01HQ8RDZQ24YBGN7PB9XQJM8JD",
                "message": {
                    "role": "assistant",
                    "content": "Latest advancements in AI include developments in natural language processing, computer vision, and reinforcement learning. For example, OpenAI's GPT-4 has shown significant improvements in understanding context and generating human-like text.",
                },
                "model_id": "openai_gpt-4o-mini",
                # "web_search_performed": True,
                # "search_results": [
                #     {
                #         "title": "Latest AI Advancements",
                #         "url": "https://example.com/latest-ai-advancements",
                #         "snippet": "Discover the latest advancements in AI, including breakthroughs in natural language processing and computer vision."
                #     },
                #     {
                #         "title": "AI Research 2023",
                #         "url": "https://example.com/ai-research-2023",
                #         "snippet": "A comprehensive overview of AI research in 2023, highlighting key papers and findings."
                #     }
                # ]
            }
        }