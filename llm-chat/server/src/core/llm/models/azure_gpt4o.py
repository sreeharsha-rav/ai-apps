from .base_llm import BaseLLM
from src.models.llm import ModelInfo, ModelID
from src.utils.decorators import singleton
from src.core.config import llm_settings
from src.core.exceptions.llm import ClientInitializationError
from typing import ClassVar
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
        """Initialize the Azure GPT-4o LLM"""
        super().__init__()
        if not self._initialized:
            self._initialize_client()
            self._initialized = True

    def _initialize_client(self):
        """Initialize the Azure GPT-4o LLM"""
        try:
            self._chat_client = AzureChatOpenAI(
                azure_endpoint=llm_settings.AZURE_OPENAI_ENDPOINT_GPT4O,
                azure_deployment=llm_settings.AZURE_OPENAI_DEPLOYMENT_GPT4O,
                api_key=llm_settings.AZURE_OPENAI_API_KEY_GPT4O,
                api_version=llm_settings.AZURE_OPENAI_API_VERSION_GPT4O,
                model=llm_settings.AZURE_OPENAI_GPT4O_MODEL,
                # temperature=0.7,
                # max_tokens=16384,
            )
        except Exception as e:
            raise ClientInitializationError(f"Failed to initialize Azure OpenAI client: {str(e)}")