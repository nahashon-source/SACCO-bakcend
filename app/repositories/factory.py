"""
Repository factory functions, used as FastAPI dependencies. Each function
checks settings.USE_MOCK_DATA once and returns the appropriate
implementation. When the real SQLAlchemy repositories exist, add the
`else` branch here — no other file changes.
"""

from app.core.config import settings
from app.repositories.mock.user_repository import MockUserRepository

_mock_user_repository = MockUserRepository()


def get_user_repository() -> MockUserRepository:
    if settings.USE_MOCK_DATA:
        return _mock_user_repository

    raise NotImplementedError(
        "Real (PostgreSQL) UserRepository is not implemented yet. "
        "Set USE_MOCK_DATA=true in .env until it is."
    )
