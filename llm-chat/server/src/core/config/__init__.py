from .settings import AppSettings, LLMSettings, SearchSettings, AzureStorageSettings

app_settings = AppSettings()
llm_settings = LLMSettings()
search_settings = SearchSettings()
azure_storage_settings = AzureStorageSettings()

__all__ = [
    "app_settings",
    "llm_settings",
    "search_settings",
    "azure_storage_settings",
]