from pydantic_settings import BaseSettings, SettingsConfigDict

class AzureStorageSettings(BaseSettings):
    """Settings for Azure Blob Storage."""
    AZURE_STORAGE_CONNECTION_STRING: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore',
        validate_assignment=True
    )

class AzureSearchSettings(BaseSettings):
    """Settings for Azure AI Search."""
    AZURE_AI_SEARCH_ENDPOINT: str
    AZURE_AI_SEARCH_API_KEY: str
    AZURE_AI_SEARCH_INDEX_NAME: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore',
        validate_assignment=True
    )

class AzureOpenAIEmbeddingSettings(BaseSettings):
    """Settings for Azure OpenAI Embedding."""
    AZURE_OPENAI_EMBEDDINGS_API_KEY: str
    AZURE_OPENAI_EMBEDDINGS_ENDPOINT: str
    AZURE_OPENAI_EMBEDDINGS_DEPLOYMENT: str
    AZURE_OPENAI_API_VERSION: str = "2023-05-15"
    AZURE_OPENAI_EMBEDDINGS_MODEL: str = "text-embedding-ada-002"

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
        extra='ignore',
        validate_assignment=True
    )

