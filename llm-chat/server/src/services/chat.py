from src.prompts.search import USE_SEARCH_RESULTS
from src.schemas.chat import Chat, ChatRequest, ChatResponse, AssistantMessage
from src.schemas.search import WebRAGResponse
from src.llm.models.base_llm import BaseLLM
from src.llm.llm_registry import LLMRegistry
from src.services.web_rag import WebRAGService
from src.repositories.chat import ChatRepository
from src.exceptions.chat import ChatNotFoundError
from src.prompts.chat import GENERAL_CHAT_PROMPT

# search
from src.schemas.search import SearchEngineID

from ulid import ULID
from typing import List
import logging


class ChatService:
    def __init__(self):
        self._llm_registry = LLMRegistry()
        self._chat_repository = ChatRepository()
        self._web_rag_service = WebRAGService()
        self.logger = logging.getLogger(__name__)       # Set up logging, remove this if not needed

    async def _handle_existing_chat(
        self, 
        chat_request: ChatRequest, 
        chat: Chat, 
        llm: BaseLLM,
    ) -> AssistantMessage:
        """Handle message processing for an existing chat."""
        assistant_message = await llm.get_completion(
            system_instruction=GENERAL_CHAT_PROMPT,
            messages=chat.messages + [chat_request.message]
        )

        # Update the chat history
        chat.messages.extend([chat_request.message, assistant_message])
        
        await self._chat_repository.update_messages(
            chat_id=chat_request.chat_id,
            messages=chat.messages
        )
        print(f"Updated chat history: {chat.messages}")
        
        return assistant_message

    async def _handle_new_chat(
        self, 
        chat_request: ChatRequest, 
        llm: BaseLLM,
    ) -> AssistantMessage:
        """Handle message processing for a new chat."""
        assistant_message = await llm.get_completion(
            system_instruction=GENERAL_CHAT_PROMPT,
            messages=[chat_request.message]
        )

        # create new chat history
        chat_history = [chat_request.message, assistant_message]
        
        new_chat = Chat(
            chat_id=chat_request.chat_id,
            title=chat_request.message.content,          # Use the user message as the title for now, TODO: improve this
            messages=chat_history,
        )
        
        await self._chat_repository.create(new_chat)
        return assistant_message

    async def generate_chat_completion(self, chat_request: ChatRequest) -> ChatResponse:
        """Generate a chat completion from a user message."""
        llm = self._llm_registry.get_model(chat_request.model_id)
        chat_exists = await self._chat_repository.chat_exists(chat_request.chat_id)

        # execute the complete web RAG process
        rag_response: WebRAGResponse = await self._web_rag_service.execute_web_rag(
            user_message=chat_request.message,
            llm=llm,
            engine_id=SearchEngineID.GOOGLE
        )

        # prepare system prompt with RAG context if available
        system_prompt = GENERAL_CHAT_PROMPT
        if rag_response.search_performed and rag_response.search_results:
            system_prompt = USE_SEARCH_RESULTS.format(
                search_results=rag_response.search_results,
                search_query=rag_response.search_query
            )

        if chat_exists:
            # handle existing chat
            existing_chat = await self._chat_repository.get(chat_request.chat_id)

            # generate completion using existing chat history
            assistant_message = await llm.get_completion(
                system_instruction=system_prompt,
                messages=existing_chat.messages + [chat_request.message]
            )

            # update the chat history
            existing_chat.messages.extend([chat_request.message, assistant_message])
            await self._chat_repository.update_messages(
                chat_id=chat_request.chat_id,
                messages=existing_chat.messages
            )
        else:
            # handle new chat
            assistant_message = await llm.get_completion(
                system_instruction=system_prompt,
                messages=[chat_request.message]
            )

            # create new chat history
            chat_history = [chat_request.message, assistant_message]
            new_chat = Chat(
                chat_id=chat_request.chat_id,
                title=chat_request.message.content,  # Use the user message as the title for now, TODO: improve this
                messages=chat_history,
            )
            await self._chat_repository.create(new_chat)

        return ChatResponse(
            chat_id=chat_request.chat_id,
            message=assistant_message,
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

    async def list_chats(self) -> List[Chat]:
        """Retrieve all chats."""
        return await self._chat_repository.list()

    async def delete_chat(self, chat_id: ULID) -> None:
        """Delete a chat by its ID."""
        await self._chat_repository.delete(chat_id)
