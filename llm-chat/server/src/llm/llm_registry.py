from typing import Dict, List
from src.llm.models.base_llm import BaseLLM
from src.schemas.llm import ModelInfo, ModelID
from src.utils.decorators import singleton
from src.llm.models.azure_gpt4o_mini import AzureGPT4oMini
from src.llm.models.azure_gpt4o import AzureGPT4o
from src.llm.models.google_gemini2_flash import GoogleGemini2Flash
from src.llm.models.openai_gpt4o_mini import OpenAIGPT4oMini
from src.exceptions.llm import ModelNotFoundError

@singleton
class LLMRegistry:
    """Registry for managing LLM models"""
    
    _models: Dict[ModelID, BaseLLM] = {
        ModelID.AZURE_GPT4O_MINI: AzureGPT4oMini(),
        ModelID.AZURE_GPT4O: AzureGPT4o(),
        ModelID.GOOGLE_GEMINI2_FLASH: GoogleGemini2Flash(),
        ModelID.OPENAI_GPT4O_MINI: OpenAIGPT4oMini(),
    }

    def list_models(self) -> List[ModelInfo]:
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