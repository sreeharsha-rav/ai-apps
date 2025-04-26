from .base_llm import BaseLLM
from src.schemas.llm import ModelInfo, ModelID
from src.utils.decorators import singleton
from src.core.config import llm_settings
from src.core.exceptions.llm import ClientInitializationError
from typing import ClassVar
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
        """Initialize the Azure GPT-4o LLM"""
        super().__init__()
        if not self._initialized:
            self._initialize_client()
            self._initialized = True

    def _initialize_client(self):
        """Initialize the OpenAI GPT-4o-mini LLM"""
        try:
            self._chat_client = ChatOpenAI(
                api_key=llm_settings.OPENAI_API_KEY,
                model=llm_settings.OPENAI_GPT4O_MINI_MODEL,
            )
        except Exception as e:
            raise ClientInitializationError(f"Failed to initialize OpenAI client: {str(e)}")
