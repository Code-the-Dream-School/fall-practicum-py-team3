"""Centralized application configuration loaded from the project .env file."""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


def _find_project_root() -> Path:
    """Locate the repository root in both editable and installed layouts.

    In an editable install ``__file__`` lives under ``services/pipeline/src/``,
    so walking up finds the repo root (which holds ``.env.example``). In a
    non-editable install the package is copied into site-packages, so fall
    back to searching upward from the current working directory, which is the
    repository root when running the test suite / CI.
    """
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".env.example").exists() or (parent / "pyproject.toml").exists():
            return parent
    cwd = Path.cwd()
    for parent in (cwd, *cwd.parents):
        if (parent / ".env.example").exists() or (parent / "pyproject.toml").exists():
            return parent
    # Last-resort default keeps the original behaviour.
    return here.parents[4]


PROJECT_ROOT = _find_project_root()


class Settings(BaseSettings):
    # Field names use snake_case; pydantic-settings matches them to the
    # UPPER_SNAKE_CASE keys in .env (e.g. openweather_api_key <- OPENWEATHER_API_KEY).
    # All optional so importing this module (and running tests) works without a .env.
    openweather_api_key: str | None = None
    supabase_url: str | None = None
    supabase_key: str | None = None
    openai_api_key: str | None = None

    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
