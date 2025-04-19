from .base_llm import BaseLLM
from src.models.llm import ModelInfo, ModelID
from src.models.chat import Message, Role
from src.utils.decorators import singleton
from src.core.config import llm_settings
from src.core.exceptions.llm import ClientInitializationError, GenerateCompletionError
from typing import ClassVar
from langchain.schema.messages import SystemMessage
from langchain_cohere.chat_models import ChatCohere


@singleton
class CohereCommandA(BaseLLM):
    """OpenAI GPT-4o-mini LLM implementation"""

    MODEL_INFO: ClassVar[ModelInfo] = ModelInfo(
        model_id=ModelID.COHERE_COMMAND_A,
        name="Command-A",
        description="A flagship model from Cohere, optimized for faster inference and lower resource usage hosted on Cohere",
        provider="Cohere",
        context_length=256000,
        max_output_tokens=8192,
    )

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            try:
                self.chat_client = ChatCohere(
                    cohere_api_key=llm_settings.COHERE_API_KEY,
                    model=llm_settings.COHERE_COMMAND_A_MODEL
                )
            except Exception as e:
                raise ClientInitializationError(f"Failed to initialize Cohere client: {str(e)}")

            self._initialized = True

    async def get_completion(self, system_instruction: str, messages: list[Message]) -> Message:
        """Get completion from Cohere Command-A model"""
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