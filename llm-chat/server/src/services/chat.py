from src.core.llm import llm_registry
from src.repositories.chat import ChatRepository
from src.core.exceptions.chat import ChatNotFoundError
from src.core.prompts import GENERAL_CHAT_SYSTEM_PROMPT
from src.schemas.chat import ChatMessageRequest, ChatMessageResponse
from src.models.chat import Chat
from src.utils.decorators import singleton
from src.utils.loggers import setup_logger
from ulid import ULID

@singleton
class ChatService:
    def __init__(self):
        self._chat_repository = ChatRepository()
        self.logger = setup_logger(name="chat")

    async def generate_chat_completion(self, chat_request: ChatMessageRequest) -> ChatMessageResponse:
        """Generate a chat completion from a user message."""
        llm = llm_registry.get_model(model_id=chat_request.model_id)
        chat_exists = await self._chat_repository.chat_exists(chat_id=chat_request.chat_id)

        if chat_exists:
            # handle existing chat
            existing_chat = await self._chat_repository.get(chat_request.chat_id)

            # generate completion using existing chat history
            ai_message = await llm.get_completion(
                system_instruction=GENERAL_CHAT_SYSTEM_PROMPT,
                messages=[
                    *existing_chat.messages,
                    chat_request.message,
                ]
            )

            # update the chat history
            existing_chat.messages.extend([chat_request.message,ai_message])
            await self._chat_repository.update_messages(
                chat_id=chat_request.chat_id,
                messages=existing_chat.messages
            )
        else:
            # handle new chat
            ai_message = await llm.get_completion(
                system_instruction=GENERAL_CHAT_SYSTEM_PROMPT,
                messages=[chat_request.message]
            )

            # create new chat history
            chat_history = [chat_request.message, ai_message]
            new_chat = Chat(
                chat_id=chat_request.chat_id,
                title=chat_request.message.content,         # Use the user message as the title, TODO: can improve this using AI generated title if possible
                messages=chat_history,
            )
            await self._chat_repository.create(new_chat)

        return ChatMessageResponse(
            chat_id=chat_request.chat_id,
            message=ai_message,
            model_id=chat_request.model_id,
            # web_search_performed=web_search_performed,
            # search_results=search_results
        )

    async def get_chat(self, chat_id: ULID) -> Chat:
        """Retrieve a chat by its ID."""
        chat = await self._chat_repository.get(chat_id)
        if chat is None:
            raise ChatNotFoundError(f"Chat with ID {chat_id} not found")
        return chat

    async def list_chats(self) -> list[Chat]:
        """Retrieve all chats."""
        return await self._chat_repository.list()

    async def delete_chat(self, chat_id: ULID) -> None:
        """Delete a chat by its ID."""
        await self._chat_repository.delete(chat_id)
