"""Centralized application configuration loaded from the project .env file."""

from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

# Project root is four levels above this file (services/pipeline/src/pipeline).
PROJECT_ROOT = Path(__file__).resolve().parents[4]


class Settings(BaseSettings):
    # Field names use snake_case; pydantic-settings matches them to the
    # UPPER_SNAKE_CASE keys in .env (e.g. openweather_api_key <- OPENWEATHER_API_KEY).
    openweather_api_key: str
    supabase_url: Optional[str] = None
    supabase_key: Optional[str] = None
    openai_api_key: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()