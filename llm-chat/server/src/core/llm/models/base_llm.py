from abc import ABC, abstractmethod
from typing import ClassVar, Optional
from src.schemas.llm import ModelInfo
from src.schemas.chat import Message, Role
from src.core.exceptions.llm import GenerateCompletionError, ClientInitializationError
from langchain.schema.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage
from langchain_core.language_models.chat_models import BaseChatModel

class BaseLLM(ABC):
    """Base class for LLM implementations"""

    MODEL_INFO: ClassVar[ModelInfo]         # Static class variable for model information

    def __init__(self):
        """Initialize the LLM"""
        self._chat_client: Optional[BaseChatModel] = None
        self._initialized = False

    @abstractmethod
    def _initialize_client(self):
        """Initialize the chat client - to be implemented by subclasses"""
        pass

    @staticmethod
    def _format_messages_for_langchain(messages: list[Message]) -> list[BaseMessage]:
        """Static method to format messages for LLM to Langchain format"""
        role_to_message = {
            Role.USER: HumanMessage,
            Role.ASSISTANT: AIMessage,
            Role.SYSTEM: SystemMessage,
        }
        return [
            role_to_message[msg.role](content=msg.content)
            for msg in messages
            if msg.role in role_to_message
        ]

    async def get_completion(self, system_instruction: str, messages: list[Message]) -> Message:
        """
        Get completion from LLM

        Args:
            system_instruction: The system instruction for the completion
            messages: The messages to use for the completion

        Returns:
            Message: The completion message

        Raises:
            ClientInitializationError: If the client is not initialized
            GenerateCompletionError: If there's an error during the completion process
        """
        try:
            if not self._chat_client and not self._initialized:
                raise ClientInitializationError("Chat client is not initialized: Initialize the client before using it")

            # format messages for Langchain
            formatted_messages = self._format_messages_for_langchain(messages)
            response = await self._chat_client.ainvoke(
                input=[
                    SystemMessage(content=system_instruction),
                    *formatted_messages,
                ]
            )
            return Message(role=Role.ASSISTANT, content=response.content)
        except Exception as e:
            raise GenerateCompletionError(f"Failed to get completion: {str(e)}")