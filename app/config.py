from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    secret_key: str
    anthropic_api_key: str  # Asegúrate de incluirlo si está en tu .env

    # Pydantic v2 usa model_config en lugar de la clase Config interna
    model_config = SettingsConfigDict(
        env_file=".env",
        extra='ignore'  # Esto permite cualquier otra variable en el .env sin lanzar error
    )

@lru_cache()
def get_settings():
    return Settings()