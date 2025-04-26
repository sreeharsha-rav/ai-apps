from src.models.llm import ModelInfo, ModelID
from src.utils.decorators import singleton
from src.core.llm.models import BaseLLM, AzureGPT4o, GoogleGemini2Flash, OpenAIGPT4oMini, CohereCommandA
from src.core.exceptions.llm import ModelNotFoundError

@singleton
class LLMRegistry:
    """Registry for managing LLM models"""
    
    _models: dict[ModelID, BaseLLM] = {
        ModelID.AZURE_GPT4O: AzureGPT4o(),
        ModelID.GOOGLE_GEMINI2_FLASH: GoogleGemini2Flash(),
        ModelID.OPENAI_GPT4O_MINI: OpenAIGPT4oMini(),
        ModelID.COHERE_COMMAND_A: CohereCommandA(),
    }

    def list_models(self) -> list[ModelInfo]:
        """List all available models"""
        return [model.MODEL_INFO for model in self._models.values()]

    def get_model_info(self, model_id: str) -> ModelInfo:
        """Get model information for a specific model"""
        try:
            model_enum = ModelID(model_id)
            return self._models[model_enum].MODEL_INFO
        except (ValueError, KeyError):
            raise ModelNotFoundError(
                f"Invalid model_id: {model_id}. "
                f"Supported models: {[m.value for m in ModelID]}"
            )

    def get_model(self, model_id: ModelID) -> BaseLLM:
        """Get the LLM instance for the specified model_id"""
        try:
            model_enum = ModelID(model_id)
            return self._models[model_enum]
        except ValueError:
            raise ModelNotFoundError(
                f"Invalid model_id: {model_id}. "
                f"Supported models: {[m.value for m in ModelID]}"
            )