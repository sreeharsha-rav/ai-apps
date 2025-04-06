from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Environment
    ENVIRONMENT: str = "development"

    # Azure Settings
    AZURE_GPT4O_MINI_API_KEY: str = ""
    AZURE_GPT4O_MINI_API_ENDPOINT: str = ""
    AZURE_GPT4O_MINI_API_VERSION: str = "2023-07-01-preview"
    AZURE_GPT4O_MINI_DEPLOYMENT: str = ""

    AZURE_GPT4O_API_KEY: str = ""
    AZURE_GPT4O_API_ENDPOINT: str = ""
    AZURE_GPT4O_API_VERSION: str = "2023-07-01-preview"
    AZURE_GPT4O_DEPLOYMENT: str = ""
    
    # Google Settings
    GOOGLE_GEMINI2_FLASH_MODEL: str = "gemini-2.0-flash-001"
    GOOGLE_GEMINI2_FLASH_API_KEY: str = ""
    
    # OpenAI Settings
    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4o-mini"

    # Search Settings
    GOOGLE_CSE_ID: str = ""
    GOOGLE_CSE_API_KEY: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=True,  # Since your vars are uppercase
        extra='ignore',       # Ignore any extra env vars
        validate_assignment=True  # Validate on assignment
    )

settings = Settings()