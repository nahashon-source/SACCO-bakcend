"""
Repository factory functions, used as FastAPI dependencies.
"""

from app.core.config import settings
from app.repositories.mock.loan_repository import MockLoanRepository
from app.repositories.mock.member_repository import MockMemberRepository
from app.repositories.mock.user_repository import MockUserRepository

_mock_user_repository = MockUserRepository()
_mock_member_repository = MockMemberRepository()
_mock_loan_repository = MockLoanRepository()


def get_user_repository() -> MockUserRepository:
    if settings.USE_MOCK_DATA:
        return _mock_user_repository
    raise NotImplementedError("Real UserRepository not implemented yet.")


def get_member_repository() -> MockMemberRepository:
    if settings.USE_MOCK_DATA:
        return _mock_member_repository
    raise NotImplementedError("Real MemberRepository not implemented yet.")


def get_loan_repository() -> MockLoanRepository:
    if settings.USE_MOCK_DATA:
        return _mock_loan_repository
    raise NotImplementedError("Real LoanRepository not implemented yet.")
