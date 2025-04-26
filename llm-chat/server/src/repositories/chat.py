from datetime import datetime
from typing import List
from src.models.chat import Chat, Message
from src.utils.decorators import singleton
from ulid import ULID
from azure.storage.blob.aio import ContainerClient
from src.core.config import azure_storage_settings
from src.core.exceptions.chat import ChatNotFoundError
from src.utils.loggers import setup_logger
from pydantic import ValidationError

@singleton
class ChatRepository:
    """Repository for managing chat objects in memory"""

    def __init__(self):
        """Initialize the ChatRepository"""
        try:
            self._chats_container_client = ContainerClient.from_connection_string(
                conn_str=azure_storage_settings.AZURE_STORAGE_CONNECTION_STRING,
                container_name=azure_storage_settings.AZURE_STORAGE_CONTAINER_NAME
            )
            # TODO: fix await - check if container exists and create if not
            # if not self._chats_container_client.exists():
            #     self._chats_container_client.create_container()
            # setup logger
            self.logger = setup_logger(name="chat_repository")
        except Exception as e:
            raise Exception(f"Failed to initialize ChatRepository Azure Blob Storage client: {str(e)}")

    @staticmethod
    def _get_chat_blob_name(chat_id: ULID) -> str:
        """Get the blob name for a chat"""
        return f"chats/{str(chat_id)}.json"

    async def create_chat_data(self, chat: Chat) -> Chat:
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
            chat_blob_client = self._chats_container_client.get_blob_client(
                blob=self._get_chat_blob_name(chat.chat_id)
            )

            if await chat_blob_client.exists():
                raise Exception(f"Chat with ID {chat.chat_id} already exists, overwrite is not allowed")

            await chat_blob_client.upload_blob(
                data=chat.model_dump_json(indent=2),
                overwrite=False
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
            blob=self._get_chat_blob_name(chat_id)
        )
        return await chat_blob_client.exists()

    async def get_chat_data(self, chat_id: ULID) -> Chat:
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
                blob=self._get_chat_blob_name(chat_id)
            )
            if await chat_blob_client.exists():
                # Download blob data and validate directly as JSON
                stream = await chat_blob_client.download_blob()
                chat_blob_data = await stream.readall()
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

    async def list_chats_data(self) -> list[Chat]:
        """
        List all chats in storage

        **Dependencies:**
        - self.get_chat_data

        Returns:
            list[Chat]: List of all chat objects

        Raises:
              Exception: If there's an error during the listing process
        """
        try:
            chats: list[Chat] = []

            # async iterator
            chat_blobs = self._chats_container_client.list_blobs(name_starts_with="chats/")
            async for blob in chat_blobs:
                # only consider JSON files
                if blob.name.endswith('.json'):
                    # get and validate chat_id
                    chat_id_str = blob.name.split('/')[-1].split('.')[0]
                    chat_id = ULID.from_str(chat_id_str)

                    # get chat data and append
                    chat = await self.get_chat_data(chat_id)
                    chats.append(chat)
            return chats
        except Exception as e:
            raise Exception(f"Failed to list chats: {str(e)}")

    async def update_chat_messages(self, chat_id: ULID, messages: List[Message]) -> Chat:
        """
        Update chat messages efficiently

        **Dependencies:**
        - self.get_chat_data

        Args:
            chat_id: The ID of the chat to update
            messages: The updated list of messages

        Returns:
            Chat: The updated chat object

        Raises:
            ValidationError: If the retrieved data does not match the expected chat structure
            ChatNotFoundError: If the chat with the given ID does not exist
            Exception: For any other unexpected errors

        Dependency: get_chat_data
        """
        try:
            chat_blob_client = self._chats_container_client.get_blob_client(
                blob=self._get_chat_blob_name(chat_id)
            )
            if await chat_blob_client.exists():
                # get existing chat data
                chat = await self.get_chat_data(chat_id)

                # update chat messages
                chat.messages = messages
                chat.updated_at = datetime.now()

                # upload updated chat data and overwrite
                await chat_blob_client.upload_blob(
                    chat.model_dump_json(), 
                    overwrite=True,
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

    async def delete_chat_data(self, chat_id: ULID) -> None:
        """
        Delete a chat if it exists

        Args:
            chat_id: The ID of the chat to delete

        Raises:
            Exception: If there's an error during the deletion process
        """
        try:
            chat_blob_client = self._chats_container_client.get_blob_client(
                blob=self._get_chat_blob_name(chat_id)
            )
            if await chat_blob_client.exists():
                await chat_blob_client.delete_blob()
        except Exception as e:
            raise Exception(f"Failed to delete chat: {str(e)}")
