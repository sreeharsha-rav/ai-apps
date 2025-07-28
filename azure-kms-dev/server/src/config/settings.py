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

    version: str = Field("0.1.0", env="VERSION")
    host: str = Field("0.0.0.0", env="SERVER_HOST")
    port: int = Field(8000, env="SERVER_PORT")
    reload: bool = Field(True, env="SERVER_RELOAD")
    log_level: str = Field("info", env="LOG_LEVEL")
    environment: Literal["development", "staging", "production"] = Field(
        default="development",
        env="ENVIRONMENT",
    )
    cors_origins: list[str] = Field(
        default=["*"],
        env="CORS_ORIGINS",
        description="List of allowed CORS origins",
    )

@lru_cache(maxsize=1)
def get_app_config() -> AppConfig:
    """Create and cache a single instance of AppConfig."""
    return AppConfig()


