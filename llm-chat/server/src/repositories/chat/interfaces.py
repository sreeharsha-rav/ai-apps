from abc import ABC
from src.models.chat import Chat
from src.repositories.base.interfaces import BaseRepository
from typing import List
from ulid import ULID

class IChatRepository(BaseRepository[Chat], ABC):
    """Interface for chat repository operations"""
    
    async def update_messages(self, chat_id: ULID, messages: List) -> Chat:
        """Update chat messages"""
        pass