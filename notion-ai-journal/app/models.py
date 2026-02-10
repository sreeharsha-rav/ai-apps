from typing import List, Optional
from pydantic import BaseModel

class ChatContext(BaseModel):
    """Represents the context of the chat."""
    user_id: Optional[str] = None
    session_id: Optional[str] = None
    items: Optional[List[str]] = None