from .base_llm import BaseLLM
from src.models.llm import ModelInfo, ModelID
from src.models.chat import Message, Role
from src.utils.decorators import singleton
from src.core.config import llm_settings
from src.core.exceptions.llm import ClientInitializationError, GenerateCompletionError
from typing import ClassVar
from langchain.schema.messages import SystemMessage
from langchain_openai import AzureChatOpenAI

@singleton
class AzureGPT4o(BaseLLM):
    """Azure GPT-4o LLM implementation"""

    MODEL_INFO: ClassVar[ModelInfo] = ModelInfo(
        model_id=ModelID.AZURE_GPT4O,
        name="GPT-4o",
        description="Flagship model from OpenAI, optimized for faster inference and lower resource usage hosted on Azure",
        provider="Azure",
        context_length=128000,
        max_output_tokens=16384,
    )

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            try:
                self.chat_client = AzureChatOpenAI(
                    azure_endpoint=llm_settings.AZURE_GPT4O_API_ENDPOINT,
                    api_key=llm_settings.AZURE_GPT4O_API_KEY,
                    api_version=llm_settings.AZURE_GPT4O_API_VERSION,
                    # temperature=0.7,
                    # max_tokens=16384,
                )
            except Exception as e:
                raise ClientInitializationError(f"Failed to initialize Azure OpenAI client: {str(e)}")

            self._initialized = True

    async def get_completion(self, system_instruction: str, messages: list[Message]) -> Message:
        """Get completion from Azure GPT-4o model"""
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