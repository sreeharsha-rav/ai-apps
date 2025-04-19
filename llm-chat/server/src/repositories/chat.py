from datetime import datetime
from typing import List
from src.models.chat import Chat, Message
from src.utils.decorators import singleton
from ulid import ULID
from azure.storage.blob import BlobServiceClient, ContentSettings
from src.core.config import azure_storage_settings
from src.core.exceptions.chat import ChatNotFoundError
from pydantic import ValidationError

@singleton
class ChatRepository:
    """Repository for managing chat objects in memory"""

    def __init__(self):
        """Initialize the ChatRepository"""
        try:
            self._chats_blob_service_client = BlobServiceClient.from_connection_string(
                conn_str=azure_storage_settings.AZURE_STORAGE_CONNECTION_STRING
            )
            self._chats_container_client = self._chats_blob_service_client.get_container_client(
                container=azure_storage_settings.AZURE_STORAGE_CONTAINER_NAME
            )
            # create container if it doesn't exist
            if not self._chats_container_client.exists():
                self._chats_container_client.create_container()
        except Exception as e:
            raise Exception(f"Failed to initialize ChatRepository Azure Blob Storage client: {str(e)}")

    def _get_blob_name(self, chat_id: ULID) -> str:
        """Get blob name with .json extension"""
        return f"{str(chat_id)}.json"

    async def create(self, chat: Chat) -> Chat:
        """
        Create a new chat

        Args:
            chat: The chat object to create

        Returns:
            Chat: The created chat object

        Raises:
            Exception: If there's an error during the creation process
        """
        try:
            # convert chat object to JSON
            chat_json = chat.model_dump_json()

            # Set content settings for JSON
            content_settings = ContentSettings(
                content_type='application/json',
                content_encoding='utf-8'
            )

            # upload to blob storage with JSON content type
            chat_blob_client = self._chats_container_client.get_blob_client(
                blob=self._get_blob_name(chat.chat_id)
            )
            chat_blob_client.upload_blob(
                chat_json, 
                overwrite=True,
                content_settings=content_settings
            )
            return chat
        except Exception as e:
            raise Exception(f"Failed to create chat: {str(e)}")

    async def chat_exists(self, chat_id: ULID) -> bool:
        """
        Check if a chat exists

        Args:
            chat_id: The ID of the chat to check

        Returns:
            bool: True if the chat exists, False otherwise
        """
        chat_blob_client = self._chats_container_client.get_blob_client(
            blob=self._get_blob_name(chat_id)
        )
        return chat_blob_client.exists()

    async def get(self, chat_id: ULID) -> Chat:
        """
        Get a chat by ID

        Args:
            chat_id: The ID of the chat to retrieve

        Returns:
            Chat: The retrieved chat object

        Raises:
            ValidationError: If the retrieved data does not match the expected chat structure
            ChatNotFoundError: If the chat with the given ID does not exist
            Exception: For any other unexpected errors
        """
        try:
            chat_blob_client = self._chats_container_client.get_blob_client(
                blob=self._get_blob_name(chat_id)
            )
            if chat_blob_client.exists():
                # Download blob data and validate directly as JSON
                chat_blob_data = chat_blob_client.download_blob().readall()
                chat = Chat.model_validate_json(chat_blob_data)
                return chat
            else:
                raise ChatNotFoundError(f"Chat with ID {chat_id} not found")
        except ValidationError as e:
            raise ValueError(f"Invalid chat data structure: {str(e)}")
        except ChatNotFoundError:
            raise # Re-raise the ChatNotFoundError as is
        except Exception as e:
            raise Exception(f"Failed to retrieve chat: {str(e)}")

    async def list(self) -> list[Chat]:
        """
        List all chats in storage

        Returns:
            list[Chat]: List of all chat objects

        Raises:
              Exception: If there's an error during the listing process
        """
        try:
            # List all blobs and filter for .json files
            chat_blobs = self._chats_container_client.list_blobs()
            chats: list[Chat] = []
            
            for blob in chat_blobs:
                # Skip non-JSON files
                if not blob.name.endswith('.json'):
                    continue
                
                chat_blob_client = self._chats_container_client.get_blob_client(blob=blob.name)
                chat_blob_data = chat_blob_client.download_blob().readall()
                chat = Chat.model_validate_json(chat_blob_data)
                chats.append(chat)
            
            return chats
        except Exception as e:
            raise Exception(f"Failed to list chats: {str(e)}")

    async def update_messages(self, chat_id: ULID, messages: List[Message]) -> Chat:
        """
        Update chat messages efficiently

        Args:
            chat_id: The ID of the chat to update
            messages: The updated list of messages

        Returns:
            Chat: The updated chat object

        Raises:
            ValidationError: If the retrieved data does not match the expected chat structure
            ChatNotFoundError: If the chat with the given ID does not exist
            Exception: For any other unexpected errors
        """
        try:
            chat_blob_client = self._chats_container_client.get_blob_client(
                blob=self._get_blob_name(chat_id)
            )
            if chat_blob_client.exists():
                # get existing chat data
                chat_blob_data = chat_blob_client.download_blob().readall()
                chat = Chat.model_validate_json(chat_blob_data)

                # update chat messages
                chat.messages = messages
                chat.updated_at = datetime.now().isoformat()

                # Set content settings for JSON
                content_settings = ContentSettings(
                    content_type='application/json',
                    content_encoding='utf-8'
                )

                # upload updated chat data and overwrite
                chat_blob_client.upload_blob(
                    chat.model_dump_json(), 
                    overwrite=True,
                    content_settings=content_settings
                )
                return chat
            else:
                raise ChatNotFoundError(f"Chat with ID {chat_id} not found")
        except ValidationError as e:
            raise ValueError(f"Invalid chat data structure: {str(e)}")
        except ChatNotFoundError:
            raise  # Re-raise the ChatNotFoundError as is
        except Exception as e:
            raise Exception(f"Failed to update chat: {str(e)}")

    async def delete(self, chat_id: ULID) -> None:
        """
        Delete a chat if it exists

        Args:
            chat_id: The ID of the chat to delete

        Raises:
            Exception: If there's an error during the deletion process
        """
        try:
            chat_blob_client = self._chats_container_client.get_blob_client(
                blob=self._get_blob_name(chat_id)
            )
            if chat_blob_client.exists():
                chat_blob_client.delete_blob()
        except Exception as e:
            raise Exception(f"Failed to delete chat: {str(e)}")
