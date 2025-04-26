from datetime import datetime
from typing import List, Optional
from src.models.chat import Chat, Message
from src.utils.decorators import singleton
from ulid import ULID
from src.core.config import storage_settings
from src.core.exceptions.chat import ChatNotFoundError
from src.repositories.base import BaseAzureBlobRepository
from .interfaces import IChatRepository

@singleton
class ChatRepository(BaseAzureBlobRepository, IChatRepository):
    """Repository for managing chat objects in Azure Blob Storage"""

    def __init__(self):
        super().__init__(storage_settings.CHAT_CONTAINER_NAME)

    @staticmethod
    def _get_chat_blob_name(chat_id: ULID) -> str:
        """Get the blob name for a chat"""
        return f"chats/{str(chat_id)}.json"

    async def create(self, chat: Chat) -> Chat:
        """Create a new chat"""
        try:
            blob_name = self._get_chat_blob_name(chat.chat_id)
            
            if await self._blob_exists(blob_name):
                raise Exception(f"Chat with ID {chat.chat_id} already exists")

            await self._upload_json(
                blob_name,
                chat.model_dump_json(indent=2),
                overwrite=False
            )
            return chat
        except Exception as e:
            raise Exception(f"Failed to create chat: {str(e)}")

    async def get(self, chat_id: ULID) -> Optional[Chat]:
        """Get a chat by ID"""
        try:
            blob_name = self._get_chat_blob_name(chat_id)
            
            if not await self._blob_exists(blob_name):
                raise ChatNotFoundError(f"Chat with ID {chat_id} not found")

            data = await self._download_json(blob_name)
            return Chat.model_validate_json(data)
        except ChatNotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to get chat: {str(e)}")

    async def list(self) -> List[Chat]:
        """List all chats"""
        try:
            chats = []
            async for blob in self._container_client.list_blobs(name_starts_with="chats/"):
                if blob.name.endswith('.json'):
                    data = await self._download_json(blob.name)
                    chats.append(Chat.model_validate_json(data))
            return chats
        except Exception as e:
            raise Exception(f"Failed to list chats: {str(e)}")

    async def delete(self, chat_id: ULID) -> None:
        """Delete a chat by ID"""
        try:
            blob_name = self._get_chat_blob_name(chat_id)
            await self._delete_blob(blob_name)
        except Exception as e:
            raise Exception(f"Failed to delete chat: {str(e)}")

    async def exists(self, chat_id: ULID) -> bool:
        """Check if a chat exists"""
        try:
            blob_name = self._get_chat_blob_name(chat_id)
            return await self._blob_exists(blob_name)
        except Exception as e:
            raise Exception(f"Failed to check chat existence: {str(e)}")

    async def update_messages(self, chat_id: ULID, messages: List[Message]) -> Chat:
        """Update chat messages"""
        try:
            chat = await self.get(chat_id)
            if not chat:
                raise ChatNotFoundError(f"Chat with ID {chat_id} not found")

            chat.messages = messages
            chat.updated_at = datetime.now()

            blob_name = self._get_chat_blob_name(chat_id)
            await self._upload_json(
                blob_name,
                chat.model_dump_json(indent=2),
                overwrite=True
            )
            return chat
        except ChatNotFoundError:
            raise
        except Exception as e:
            raise Exception(f"Failed to update chat messages: {str(e)}")