from .settings import AppSettings, LLMSettings, SearchSettings

app_settings = AppSettings()
llm_settings = LLMSettings()
search_settings = SearchSettings()

__all__ = [
    "app_settings",
    "llm_settings",
    "search_settings",
]