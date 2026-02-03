from pydantic import BaseModel, Field
from typing import List, Optional, Any
from datetime import datetime
from ulid import ULID

class CanvasItem(BaseModel):
    id: str = Field(default_factory=lambda: str(ULID()))
    type: str # e.g., "product_list", "product_detail", "markdown"
    content: Any

class CanvasData(BaseModel):
    items: List[CanvasItem] = Field(default_factory=list)

class Item(BaseModel):
    id: str = Field(default_factory=lambda: str(ULID()))
    data: Any
    timestamp: datetime = Field(default_factory=datetime.now)

class ChatHistory(BaseModel):
    id: str = Field(default_factory=lambda: str(ULID()))
    title: str = "New Chat"
    items: List[Item] = Field(default_factory=list)
    canvas: Optional[CanvasData] = None # Canvas state is now at chat level
    total_tokens: int = 0
    updated_at: datetime = Field(default_factory=datetime.now)
    created_at: datetime = Field(default_factory=datetime.now)

class ChatRequest(BaseModel):
    prompt: str = Field(
        ...,
        min_length=1, 
        pattern="^.+",
        examples=[
            "Hello, how are you?"
        ]
    )
    model: str = Field(default="gpt-5-mini")
    chat_id: Optional[str] = Field(
        ...,
        examples=[
            "01A1B2C3D4E5F6G7H8I9J0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6"
        ]
    )

