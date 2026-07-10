"""
Repository factory functions, used as FastAPI dependencies. Each checks
settings.USE_MOCK_DATA once and returns the appropriate implementation.
"""

from app.core.config import settings
from app.repositories.mock.member_repository import MockMemberRepository
from app.repositories.mock.user_repository import MockUserRepository

_mock_user_repository = MockUserRepository()
_mock_member_repository = MockMemberRepository()


def get_user_repository() -> MockUserRepository:
    if settings.USE_MOCK_DATA:
        return _mock_user_repository

    raise NotImplementedError(
        "Real (PostgreSQL) UserRepository is not implemented yet. "
        "Set USE_MOCK_DATA=true in .env until it is."
    )


def get_member_repository() -> MockMemberRepository:
    if settings.USE_MOCK_DATA:
        return _mock_member_repository

    raise NotImplementedError(
        "Real (PostgreSQL) MemberRepository is not implemented yet. "
        "Set USE_MOCK_DATA=true in .env until it is."
    )
