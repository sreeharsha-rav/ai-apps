from .settings import AppSettings, LLMSettings, SearchSettings, StorageSettings

app_settings = AppSettings()
llm_settings = LLMSettings()
search_settings = SearchSettings()
storage_settings = StorageSettings()

__all__ = [
    "app_settings",
    "llm_settings",
    "search_settings",
    "storage_settings",
]