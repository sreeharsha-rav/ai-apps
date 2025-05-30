from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, AnyUrl
from enum import Enum


class Environment(str, Enum):
    """Environment settings for the application."""
    DEVELOPMENT = "development"
    PRODUCTION = "production"

class AppSettings(BaseSettings):
    ENVIRONMENT: Environment = Field(
        default=Environment.DEVELOPMENT,
        description="Running environment (development/production)"
    )
    HOST: str = "127.0.0.1"
    PORT: int = 8020

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

class LLMSettings(BaseSettings):
    """Settings for all LLMs"""
    # Azure LLM Settings
    AZURE_OPENAI_API_KEY_GPT4O: str = ""
    AZURE_OPENAI_ENDPOINT_GPT4O: str = ""
    AZURE_OPENAI_DEPLOYMENT_GPT4O: str = ""
    AZURE_OPENAI_API_VERSION_GPT4O: str = "2024-12-01-preview"
    AZURE_OPENAI_GPT4O_MODEL: str = "gpt-4o"
    # Google LLM Settings
    GOOGLE_GEMINI2_FLASH_MODEL: str = "gemini-2.0-flash-001"
    GOOGLE_GEMINI2_FLASH_API_KEY: str = ""
    # OpenAI LLM Settings
    OPENAI_API_KEY: str = ""
    OPENAI_GPT4O_MINI_MODEL: str = "gpt-4o-mini"
    # Cohere LLM Settings
    COHERE_API_KEY: str = ""
    COHERE_COMMAND_A_MODEL: str = "command-a-03-2025"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
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
        env_file_encoding="utf-8",
        extra="allow",
    )

class StorageSettings(BaseSettings):
    """Settings for Storage"""
    AZURE_STORAGE_CONNECTION_STRING: str = ""
    # Container name for storing chat objects
    CHAT_CONTAINER_NAME: str = ""
    # Container name for storing space objects
    SPACE_CONTAINER_NAME: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )

class AuthSettings(BaseSettings):
    """Settings for authentication"""
    MICROSOFT_CLIENT_ID: str = ""
    MICROSOFT_JWKS_URL: str = "https://login.microsoftonline.com/common/discovery/keys"
    GOOGLE_CLIENT_ID: str = ""
    GOOGLE_JWKS_URL: str = "https://www.googleapis.com/oauth2/v3/certs"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="allow",
    )