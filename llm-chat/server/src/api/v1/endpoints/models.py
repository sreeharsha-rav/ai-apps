from fastapi import APIRouter, status, Path
from src.core.llm import llm_registry
from src.schemas.llm import ModelInfo, ModelID

models_router = APIRouter(
    prefix="/models",
    tags=["models"],
)

@models_router.get("", response_model=list[ModelInfo], status_code=status.HTTP_200_OK)
async def list_models() -> list[ModelInfo]:
    """List all available models"""
    return llm_registry.list_models()

@models_router.get("/{model_id}", response_model=ModelInfo, status_code=status.HTTP_200_OK)
async def get_model_info(model_id: ModelID = Path(description="The model ID to get information for")) -> ModelInfo:
    """Get model information for a specific model"""
    return llm_registry.get_model_info(model_id)