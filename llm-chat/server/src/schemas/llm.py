from enum import Enum
from pydantic import BaseModel, Field

class ModelID(str, Enum):
    """Enum for supported model IDs"""
    AZURE_GPT4O_MINI = "azure_gpt-4o-mini"
    AZURE_GPT4O = "azure_gpt-4o"
    GOOGLE_GEMINI2_FLASH = "google_gemini-2.0-flash"
    OPENAI_GPT4O_MINI = "openai_gpt-4o-mini"

class ModelInfo(BaseModel):
    """Information about the model"""
    model_id: str = Field(description="Unique identifier for the model")
    name: str = Field(description="Display name for the model")
    provider: str = Field(description="Model provider e.g. OpenAI, Azure, Google")
    description: str = Field(description="Detailed description of the model")
    context_length: int = Field(gt=0, description="Context window length for the model")
    max_output_tokens: int = Field(gt=0, description="Maximum output tokens for the model")