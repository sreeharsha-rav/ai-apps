from .settings import AzureStorageSettings, AzureSearchSettings, AzureOpenAIEmbeddingSettings
from .constants import TEMP_DIR, CHUNK_SIZE, CHUNK_OVERLAP

azure_storage_settings = AzureStorageSettings()
azure_search_settings = AzureSearchSettings()
azure_openai_embedding_settings = AzureOpenAIEmbeddingSettings()

__all__ = [
    "azure_storage_settings",
    "azure_search_settings",
    "azure_openai_embedding_settings",
    "TEMP_DIR",
    "CHUNK_SIZE",
    "CHUNK_OVERLAP"
]