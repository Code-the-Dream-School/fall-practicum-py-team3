import os
from pathlib import Path

import pytest

from pipeline.config import Settings, PROJECT_ROOT

ENV_EXAMPLE = PROJECT_ROOT / ".env.example"


def _env_example_keys():
    keys = []
    for line in ENV_EXAMPLE.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        keys.append(line.split("=", 1)[0].strip())
    return keys


@pytest.mark.skipif(
    not os.getenv("OPENWEATHER_API_KEY"),
    reason="OPENWEATHER_API_KEY not set",
)
def test_openweather_api_key_loaded():
    settings = Settings()
    assert settings.openweather_api_key is not None
    assert len(settings.openweather_api_key) > 0


def test_env_example_matches_config_fields():
    # Every key in .env.example must be a field in Settings (and vice versa).
    example_keys = {k.lower() for k in _env_example_keys()}
    # pydantic-settings maps UPPER_SNAKE_CASE env keys to snake_case fields.
    field_names = {name.lower() for name in Settings.model_fields}
    assert example_keys == field_names, (
        f".env.example keys {sorted(example_keys)} != Settings fields {sorted(field_names)}"
    )