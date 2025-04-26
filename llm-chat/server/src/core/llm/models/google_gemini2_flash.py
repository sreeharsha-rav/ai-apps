from .base_llm import BaseLLM
from src.models.llm import ModelInfo, ModelID
from src.utils.decorators import singleton
from src.core.config import llm_settings
from src.core.exceptions.llm import ClientInitializationError
from typing import ClassVar
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
        """Initialize the Azure GPT-4o LLM"""
        super().__init__()
        if not self._initialized:
            self._initialize_client()
            self._initialized = True

    def _initialize_client(self):
        """Initialize the Google Gemini 2.0 Flash LLM"""
        try:
            self._chat_client = ChatGoogleGenerativeAI(
                model=llm_settings.GOOGLE_GEMINI2_FLASH_MODEL,
                api_key=llm_settings.GOOGLE_GEMINI2_FLASH_API_KEY,
            )
        except Exception as e:
            raise ClientInitializationError(f"Failed to initialize Google Gemini client: {str(e)}")