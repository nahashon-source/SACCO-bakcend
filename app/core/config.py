"""
Central application configuration.
"""

from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    APP_NAME: str = "SACCO Management System API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    USE_MOCK_DATA: bool = True

    DATABASE_URL: str = ""

    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # Comma-separated string in the environment (e.g.
    # "https://a.com,https://b.com"), parsed into a list here. This is
    # deliberately NOT a list[str] field — JSON-syntax env vars are
    # fragile across different dashboard UIs (quote mangling, escaping
    # differences between Render/Docker/.env files). A plain
    # comma-separated string has no such ambiguity.
    CORS_ALLOWED_ORIGINS: str = "http://localhost:5173"

    @field_validator("CORS_ALLOWED_ORIGINS")
    @classmethod
    def strip_origins(cls, value: str) -> str:
        return value.strip()

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.CORS_ALLOWED_ORIGINS.split(",") if origin.strip()]

    REDIS_URL: str = ""
    RATE_LIMIT_PER_MINUTE: int = 60

    API_V1_PREFIX: str = "/api/v1"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
