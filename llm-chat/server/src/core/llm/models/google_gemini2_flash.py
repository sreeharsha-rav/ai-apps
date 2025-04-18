from .base_llm import BaseLLM
from src.models.llm import ModelInfo, ModelID
from src.models.chat import Message, Role
from src.utils.decorators import singleton
from src.core.config import llm_settings
from src.core.exceptions.llm import ClientInitializationError, GenerateCompletionError
from typing import ClassVar
from langchain.schema.messages import SystemMessage
from langchain_google_genai.chat_models import ChatGoogleGenerativeAI

@singleton
class GoogleGemini2Flash(BaseLLM):
    """Google Gemini 2.0 Flash LLM implementation"""

    MODEL_INFO: ClassVar[ModelInfo] = ModelInfo(
        model_id=ModelID.GOOGLE_GEMINI2_FLASH,
        name="Gemini 2.0 Flash",
        description="A flash-optimized version of the Gemini 2.0 model, designed for faster inference and lower resource usage hosted on Google",
        provider="Google",
        context_length=1048576,
        max_output_tokens=8192,
    )

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            try:
                self.chat_client = ChatGoogleGenerativeAI(
                    model=llm_settings.GOOGLE_GEMINI2_FLASH_MODEL,
                    api_key=llm_settings.GOOGLE_GEMINI2_FLASH_API_KEY,
                )
            except Exception as e:
                raise ClientInitializationError(f"Failed to initialize Google Gemini client: {str(e)}")
                
            self._initialized = True

    async def get_completion(self, system_instruction: str, messages: list[Message]) -> Message:
        """Get completion from Google Gemini 2.0 Flash model"""
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
