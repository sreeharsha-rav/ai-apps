from abc import ABC, abstractmethod
from src.models.chat import Chat, Message
from typing import Optional
from ulid import ULID

class IChatRepository(ABC):
    """Interface for chat repository operations"""

    @abstractmethod
    async def chat_exists(self, chat_id: ULID) -> bool:
        """Check if a chat exists"""
        pass

    @abstractmethod
    async def create_chat(self, chat: Chat) -> Chat:
        """Create a new chat"""
        pass

    @abstractmethod
    async def get_chat_by_id(self, chat_id: ULID) -> Optional[Chat]:
        """Get a chat by ID"""
        pass

    @abstractmethod
    async def list_all_chats(self) -> list[Chat]:
        """List all chats"""
        pass

    @abstractmethod
    async def delete_chat_by_id(self, chat_id: ULID) -> None:
        """Delete a chat by ID"""
        pass

    @abstractmethod
    async def update_messages(self, chat_id: ULID, messages: list[Message]) -> Chat:
        """Update chat messages"""
        pass