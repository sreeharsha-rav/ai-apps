from abc import ABC, abstractmethod
from typing import ClassVar
from src.schemas.llm import ModelInfo
from src.schemas.chat import Message, AssistantMessage
from typing import List

class BaseLLM(ABC):
    """Base class for LLM implementations"""

    MODEL_INFO: ClassVar[ModelInfo]         # Static class variable for model information

    def __init__(self) -> None:
        """Initialize the LLM"""
        pass

    @abstractmethod
    async def get_completion(self, system_instruction: str, messages: List[Message]) -> AssistantMessage:
        """Get completion from LLM"""
        pass