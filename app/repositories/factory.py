"""
Repository factory functions, used as FastAPI dependencies.
"""

from app.core.config import settings
from app.repositories.mock.contribution_repository import MockContributionRepository
from app.repositories.mock.guarantor_repository import MockGuarantorRepository
from app.repositories.mock.loan_repository import MockLoanRepository
from app.repositories.mock.member_repository import MockMemberRepository
from app.repositories.mock.savings_repository import MockSavingsRepository
from app.repositories.mock.shares_repository import MockSharesRepository
from app.repositories.mock.user_repository import MockUserRepository

_mock_user_repository = MockUserRepository()
_mock_member_repository = MockMemberRepository()
_mock_loan_repository = MockLoanRepository()
_mock_savings_repository = MockSavingsRepository()
_mock_shares_repository = MockSharesRepository()
_mock_guarantor_repository = MockGuarantorRepository()
_mock_contribution_repository = MockContributionRepository()


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


def get_savings_repository() -> MockSavingsRepository:
    if settings.USE_MOCK_DATA:
        return _mock_savings_repository
    raise NotImplementedError("Real SavingsRepository not implemented yet.")


def get_shares_repository() -> MockSharesRepository:
    if settings.USE_MOCK_DATA:
        return _mock_shares_repository
    raise NotImplementedError("Real SharesRepository not implemented yet.")


def get_guarantor_repository() -> MockGuarantorRepository:
    if settings.USE_MOCK_DATA:
        return _mock_guarantor_repository
    raise NotImplementedError("Real GuarantorRepository not implemented yet.")


def get_contribution_repository() -> MockContributionRepository:
    if settings.USE_MOCK_DATA:
        return _mock_contribution_repository
    raise NotImplementedError("Real ContributionRepository not implemented yet.")


from app.repositories.mock.transaction_repository import MockTransactionRepository

_mock_transaction_repository = MockTransactionRepository()


def get_transaction_repository() -> MockTransactionRepository:
    if settings.USE_MOCK_DATA:
        return _mock_transaction_repository
    raise NotImplementedError("Real TransactionRepository not implemented yet.")


from app.repositories.mock.notification_repository import MockNotificationRepository

_mock_notification_repository = MockNotificationRepository()


def get_notification_repository() -> MockNotificationRepository:
    if settings.USE_MOCK_DATA:
        return _mock_notification_repository
    raise NotImplementedError("Real NotificationRepository not implemented yet.")
