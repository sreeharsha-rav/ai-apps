from pydantic_settings import BaseSettings, SettingsConfigDict

class AppSettings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "development"
    PORT: int = 8000
    HOST: str = "127.0.0.1"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,  # Since your vars are uppercase
        extra='ignore',       # Ignore any extra env vars
        validate_assignment=True  # Validate on assignment
    )

class LLMSettings(BaseSettings):
    """Settings for all LLMs"""
    # Azure LLM Settings
    AZURE_GPT4O_MINI_API_KEY: str = ""
    AZURE_GPT4O_MINI_API_ENDPOINT: str = ""
    AZURE_GPT4O_MINI_API_VERSION: str = "2023-07-01-preview"
    AZURE_GPT4O_MINI_DEPLOYMENT: str = ""

    AZURE_GPT4O_API_KEY: str = ""
    AZURE_GPT4O_API_ENDPOINT: str = ""
    AZURE_GPT4O_API_VERSION: str = "2023-07-01-preview"
    AZURE_GPT4O_DEPLOYMENT: str = ""

    # Google LLM Settings
    GOOGLE_GEMINI2_FLASH_MODEL: str = "gemini-2.0-flash-001"
    GOOGLE_GEMINI2_FLASH_API_KEY: str = ""

    # OpenAI LLM Settings
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,  # Since your vars are uppercase
        extra='ignore',       # Ignore any extra env vars
        validate_assignment=True  # Validate on assignment
    )

class SearchSettings(BaseSettings):
    """Settings for all search engines"""
    # Google Search Settings
    GOOGLE_CSE_ID: str = ""
    GOOGLE_CSE_API_KEY: str = ""
    GOOGLE_CSE_BASE_URL: str = "https://www.googleapis.com/customsearch/v1"

    # DuckDuckGo Search Settings
    # TODO: Add DuckDuckGo search settings

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,  # Since your vars are uppercase
        extra='ignore',       # Ignore any extra env vars
        validate_assignment=True  # Validate on assignment
    )