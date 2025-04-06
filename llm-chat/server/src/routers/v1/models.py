from fastapi import APIRouter, status, Path
from src.llm.llm_registry import LLMRegistry
from src.schemas.llm import ModelInfo, ModelID
from typing import List

router = APIRouter(
    prefix="/v1/models",
    tags=["models"],
)

llm_registry = LLMRegistry()

@router.get("", response_model=List[ModelInfo], status_code=status.HTTP_200_OK)
def list_models() -> List[ModelInfo]:
    """List all available models"""
    return llm_registry.list_models()

@router.get("/{model_id}", response_model=ModelInfo, status_code=status.HTTP_200_OK)
def get_model_info(model_id: ModelID = Path(description="The model ID to get information for")) -> ModelInfo:
    """Get model information for a specific model"""
    return llm_registry.get_model_info(model_id)