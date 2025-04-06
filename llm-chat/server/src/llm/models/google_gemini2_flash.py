from src.llm.models.base_llm import BaseLLM
from src.schemas.llm import ModelInfo, ModelID
from src.schemas.chat import Role, Message, AssistantMessage
from src.utils.decorators import singleton
from src.config.settings import settings
from src.exceptions.llm  import ConfigurationError, ClientInitializationError, GenerateCompletionError
from typing import ClassVar, List
from google.genai import Client, types

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
            
            # Validate required environment variables
            self.model = settings.GOOGLE_GEMINI2_FLASH_MODEL
            
            if not self.model:
                raise ConfigurationError("GOOGLE_GEMINI2_FLASH_MODEL environment variable is not set")
            
            try:
                self.client = Client(
                    api_key=settings.GOOGLE_GEMINI2_FLASH_API_KEY,
                )
            except Exception as e:
                raise ClientInitializationError(f"Failed to initialize Google Gemini client: {str(e)}")
                
            self._initialized = True

    async def get_completion(self, system_instruction: str, messages: List[Message]) -> AssistantMessage:
        """Get completion from Google Gemini 2.0 Flash model"""
        try:
            # format messages for Gemini
            chat_history = [
                types.Content(
                    role=("user" if message.role == Role.USER else "model"),
                    parts=[
                        types.Part(
                            text=message.content
                        )
                    ]
                ) for message in messages
            ]

            response = self.client.models.generate_content(
                model=self.model,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction
                ),
                contents=chat_history
            )

            return AssistantMessage(
                role=Role.ASSISTANT,
                content=response.text
            )
        except Exception as e:
            raise GenerateCompletionError(f"Failed to get completion: {str(e)}")
