from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    api_key: str = "minha-chave-secreta-dev"
    time_limit_max_segundos: int = 120
    app_name: str = "Cutting Stock Optimizer API"
    app_version: str = "1.0.0"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings():
    return Settings()

settings = get_settings()

API_KEY = settings.api_key
