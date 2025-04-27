from datetime import datetime
from typing import Optional
from src.models.chat import Chat, Message
from src.utils.decorators import singleton
from ulid import ULID
from src.core.config import storage_settings
from .interfaces import IChatRepository
from azure.storage.blob.aio import ContainerClient, BlobClient

@singleton
class ChatRepository(IChatRepository):
    """Repository for managing chat objects in Azure Blob Storage"""

    def __init__(self):
        self._chat_container_client = ContainerClient.from_connection_string(
            conn_str=storage_settings.AZURE_STORAGE_CONNECTION_STRING,
            container_name=storage_settings.CHAT_CONTAINER_NAME
        )

    def _get_chat_blob_client(self, chat_id: ULID) -> BlobClient:
        """Get the blob client for a chat"""
        blob_name = f"chats/{str(chat_id)}.json"
        return self._chat_container_client.get_blob_client(blob=blob_name)

    async def chat_exists(self, chat_id: ULID) -> bool:
        """Check if a chat exists"""
        chat_blob_client = self._get_chat_blob_client(chat_id)
        return await chat_blob_client.exists()

    async def create_chat(self, chat: Chat) -> Chat:
        """Create a new chat"""
        chat_blob_client = self._get_chat_blob_client(chat.chat_id)
        await chat_blob_client.upload_blob(
            data=chat.model_dump_json(indent=2),
            overwrite=False
        )
        return chat

    async def get_chat_by_id(self, chat_id: ULID) -> Optional[Chat]:
        """Get a chat by ID"""
        chat_blob_client = self._get_chat_blob_client(chat_id)
        chat_stream = await chat_blob_client.download_blob()
        chat_data = await chat_stream.readall()
        chat = Chat.model_validate_json(chat_data)
        return chat

    async def list_all_chats(self) -> list[Chat]:
        """List all chats"""
        chats = []
        async for blob in self._chat_container_client.list_blobs(name_starts_with="chats/", delimiter=".json"):
            stream = await blob.download_blob()
            data = await stream.readall()
            chats.append(Chat.model_validate_json(data))
        return chats

    async def delete_chat_by_id(self, chat_id: ULID) -> None:
        """Delete a chat by ID"""
        chat_blob_client = self._get_chat_blob_client(chat_id)
        await chat_blob_client.delete_blob()

    async def update_messages(self, chat_id: ULID, messages: list[Message]) -> Chat:
        """Update chat messages"""
        chat_blob_client = self._get_chat_blob_client(chat_id)
        chat_stream = await chat_blob_client.download_blob()
        chat_data = await chat_stream.readall()
        chat = Chat.model_validate_json(chat_data)
        chat.messages = messages
        chat.updated_at = datetime.now()
        await chat_blob_client.upload_blob(
            data=chat.model_dump_json(indent=2),
            overwrite=True
        )
        return chat