from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class AppConfig(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    VERSION: str = "1.0.0"
    ENVIRONMENT: Literal["development", "staging", "production"] = "development"
    SERVER_HOST: str = "0.0.0.0"
    SERVER_PORT: int = 8080
    SERVER_RELOAD: bool = True
    SERVER_LOG_LEVEL: Literal["debug", "info", "warning", "error", "critical"] = "debug"
    CORS_ORIGINS: list[str] = Field(
        default=["*"],
        description="List of allowed CORS origins"
    )

class StorageSettings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=True,
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    AZURE_STORAGE_CONTAINER_NAME: str = "user-uploads"
    AZURE_STORAGE_CONNECTION_STRING: str = ""

@lru_cache(maxsize=1)
def get_app_config() -> AppConfig:
    """Create and cache a single instance of AppConfig."""
    return AppConfig()

@lru_cache(maxsize=1)
def get_storage_settings() -> StorageSettings:
    """Create and cache a single instance of StorageSettings."""
    return StorageSettings()


