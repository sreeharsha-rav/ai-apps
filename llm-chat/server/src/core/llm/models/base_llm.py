from abc import ABC, abstractmethod
from typing import ClassVar
from src.models.llm import ModelInfo
from src.schemas.chat import Message, Role
from langchain.schema.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage

class BaseLLM(ABC):
    """Base class for LLM implementations"""

    MODEL_INFO: ClassVar[ModelInfo]         # Static class variable for model information

    def __init__(self):
        """Initialize the LLM"""
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

    @abstractmethod
    async def get_completion(self, system_instruction: str, messages: list[Message]) -> Message:
        """Get completion from LLM"""
        pass