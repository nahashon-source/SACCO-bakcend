"""
Central application configuration.

All environment-dependent values must be read through this module —
never call os.getenv() directly elsewhere in the codebase. This keeps
configuration auditable in one place and validated at startup (Pydantic
will raise immediately on a missing/malformed required value, rather than
failing confusingly deep inside a request handler later).
"""

from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )

    # --- App metadata ---
    APP_NAME: str = "SACCO Management System API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    # --- Data source toggle ---
    USE_MOCK_DATA: bool = True

    # --- Database (only required when USE_MOCK_DATA=False) ---
    DATABASE_URL: str = ""

    # --- JWT / Auth ---
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    # --- CORS ---
    CORS_ALLOWED_ORIGINS: list[str] = ["http://localhost:5173"]

    # --- Redis / rate limiting / background jobs ---
    # Empty string = Redis-backed features (rate limiting, caching, Celery)
    # are disabled and no-op safely. Set once Redis is actually reachable
    # (Docker locally, or a managed Redis instance on Render).
    REDIS_URL: str = ""
    RATE_LIMIT_PER_MINUTE: int = 60

    # --- API ---
    API_V1_PREFIX: str = "/api/v1"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
