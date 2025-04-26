from .base_llm import BaseLLM
from src.models.llm import ModelInfo, ModelID
from src.utils.decorators import singleton
from src.core.config import llm_settings
from src.core.exceptions.llm import ClientInitializationError
from typing import ClassVar
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
        """Initialize the Azure GPT-4o LLM"""
        super().__init__()
        if not self._initialized:
            self._initialize_client()
            self._initialized = True

    def _initialize_client(self):
        """Initialize Cohere Command-A LLM"""
        try:
            self._chat_client = ChatCohere(
                cohere_api_key=llm_settings.COHERE_API_KEY,
                model=llm_settings.COHERE_COMMAND_A_MODEL
            )
        except Exception as e:
            raise ClientInitializationError(f"Failed to initialize Cohere client: {str(e)}")
