from datetime import datetime
from typing import Dict, List, Optional
from src.schemas.chat import Chat, Message
from src.utils.decorators import singleton
from ulid import ULID

@singleton
class ChatRepository:
    """Repository for managing chat objects in memory"""

    def __init__(self):
        self._chats: Dict[ULID, Chat] = {}

    async def create(self, chat: Chat) -> Chat:
        """Create a new chat"""
        chat.updated_at = datetime.now().isoformat()
        self._chats[chat.chat_id] = chat
        return chat

    async def chat_exists(self, chat_id: ULID) -> bool:
        """Check if a chat exists"""
        return chat_id in self._chats

    async def get(self, chat_id: ULID) -> Optional[Chat]:
        """Get a chat by ID"""
        return self._chats.get(chat_id)

    async def list(self) -> List[Chat]:
        """List all chats"""
        return list(self._chats.values())

    async def update_messages(self, chat_id: ULID, messages: List[Message]) -> Chat:
        """Update chat messages efficiently"""
        if chat_id not in self._chats:
            raise KeyError(f"Chat with ID {chat_id} not found")

        chat = self._chats[chat_id]
        chat.messages = messages
        chat.updated_at = datetime.now().isoformat()
        return chat

    async def delete(self, chat_id: ULID) -> None:
        """Delete a chat"""
        if chat_id in self._chats:
            del self._chats[chat_id]
