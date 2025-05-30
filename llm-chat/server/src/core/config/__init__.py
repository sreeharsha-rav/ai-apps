from .settings import AppSettings, LLMSettings, SearchSettings, StorageSettings, Environment

app_settings = AppSettings()
llm_settings = LLMSettings()
search_settings = SearchSettings()
storage_settings = StorageSettings()

__all__ = [
    "Environment",
    "app_settings",
    "llm_settings",
    "search_settings",
    "storage_settings",
]