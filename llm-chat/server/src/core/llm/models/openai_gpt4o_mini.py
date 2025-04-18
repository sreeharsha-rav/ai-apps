from .base_llm import BaseLLM
from src.models.llm import ModelInfo, ModelID
from src.models.chat import Message, Role
from src.utils.decorators import singleton
from src.core.config import llm_settings
from src.core.exceptions.llm import ClientInitializationError, GenerateCompletionError
from typing import ClassVar
from langchain.schema.messages import SystemMessage
from langchain_openai.chat_models import ChatOpenAI

@singleton
class OpenAIGPT4oMini(BaseLLM):
    """OpenAI GPT-4o-mini LLM implementation"""

    MODEL_INFO: ClassVar[ModelInfo] = ModelInfo(
        model_id=ModelID.OPENAI_GPT4O_MINI,
        name="GPT-4o mini",
        description="A smaller version of the GPT-4o model, optimized for faster inference and lower resource usage hosted on OpenAI",
        provider="OpenAI",
        context_length=128000,
        max_output_tokens=16384,
    )

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            try:
                self.chat_client = ChatOpenAI(
                    api_key=llm_settings.OPENAI_API_KEY,
                    model=llm_settings.OPENAI_MODEL,
                )
            except Exception as e:
                raise ClientInitializationError(f"Failed to initialize OpenAI client: {str(e)}")
            
            self._initialized = True

    async def get_completion(self, system_instruction: str, messages: list[Message]) -> Message:
        """Get completion from OpenAI GPT-4o-mini model"""
        try:
            # format messages for Langchain
            formatted_messages = self._format_messages_for_langchain(messages)
            response = self.chat_client.invoke(
                input=[
                    SystemMessage(content=system_instruction),
                    *formatted_messages,
                ]
            )
            return Message(role=Role.ASSISTANT, content=response.content)
        except Exception as e:
            raise GenerateCompletionError(f"Failed to get completion: {str(e)}")
