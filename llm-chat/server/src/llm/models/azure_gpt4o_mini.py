from src.llm.models.base_llm import BaseLLM
from src.schemas.llm import ModelInfo, ModelID
from src.schemas.chat import Role, Message, AssistantMessage
from src.utils.decorators import singleton
from src.config.settings import settings
from src.exceptions.llm import ConfigurationError, ClientInitializationError, GenerateCompletionError
from typing import ClassVar, List
from openai import AzureOpenAI

@singleton
class AzureGPT4oMini(BaseLLM):
    """Azure GPT-4o-mini LLM implementation"""

    MODEL_INFO: ClassVar[ModelInfo] = ModelInfo(
        model_id=ModelID.AZURE_GPT4O_MINI,
        name="GPT-4o mini",
        description="A smaller version of the GPT-4o model, optimized for faster inference and lower resource usage hosted on Azure",
        provider="Azure",
        context_length=128000,
        max_output_tokens=16384,
    )

    def __init__(self):
        if not hasattr(self, '_initialized'):
            super().__init__()
            
            # Validate required environment variables
            self.api_key = settings.AZURE_GPT4O_MINI_API_KEY
            self.endpoint = settings.AZURE_GPT4O_MINI_API_ENDPOINT
            self.api_version = settings.AZURE_GPT4O_MINI_API_VERSION
            self.deployment = settings.AZURE_GPT4O_MINI_DEPLOYMENT

            if not self.api_key:
                raise ConfigurationError("AZURE_GPT4O_MINI_API_KEY environment variable is not set")
            if not self.endpoint:
                raise ConfigurationError("AZURE_GPT4O_MINI_API_ENDPOINT environment variable is not set")
            if not self.api_version:
                raise ConfigurationError("AZURE_GPT4O_MINI_API_VERSION environment variable is not set")
            if not self.deployment:
                raise ConfigurationError("AZURE_GPT4O_MINI_DEPLOYMENT environment variable is not set")

            try:
                self.client = AzureOpenAI(
                    azure_endpoint=self.endpoint,
                    api_key=self.api_key,
                    api_version=self.api_version,
                )
            except Exception as e:
                raise ClientInitializationError(f"Failed to initialize Azure OpenAI client: {str(e)}")
                
            self._initialized = True

    async def get_completion(self, system_instruction: str, messages: List[Message]) -> AssistantMessage:
        """Get completion from Azure GPT-4o-mini model"""
        try:
            formatted_messages = [
                {"role": Role.SYSTEM, "content": system_instruction}       # Add system message first
            ]
            # Extend the list directly instead of using unpacking
            formatted_messages.extend(
                message.model_dump(include={"role", "content"}) 
                for message in messages
            )
            
            response = self.client.chat.completions.create(
                model=self.deployment,
                messages=formatted_messages,
            )

            return AssistantMessage(
                role=Role.ASSISTANT,
                content=response.choices[0].message.content
            )
        except Exception as e:
            raise GenerateCompletionError(f"Failed to get completion: {str(e)}")
