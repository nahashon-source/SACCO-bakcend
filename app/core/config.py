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
    ENVIRONMENT: str = "development"  # development | staging | production
    DEBUG: bool = True

    # --- Data source toggle ---
    # When True, all repositories use in-memory mock data (see app/repositories/mock/).
    # When False, repositories use the real SQLAlchemy/PostgreSQL implementation.
    # This is the single switch that flips the entire persistence layer.
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

    # --- Redis / background jobs (only required once workers are wired in) ---
    REDIS_URL: str = ""

    # --- API ---
    API_V1_PREFIX: str = "/api/v1"


@lru_cache
def get_settings() -> Settings:
    """
    Cached settings accessor. FastAPI's dependency injection will call this
    repeatedly per-request; lru_cache ensures the .env file is parsed once,
    not on every call.
    """
    return Settings()


settings = get_settings()
