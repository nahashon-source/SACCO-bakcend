"""
Repository factory functions, used as FastAPI dependencies. Each checks
settings.USE_MOCK_DATA once and returns the appropriate implementation.
When real SQLAlchemy repositories exist, add the else branch here —
no other file changes.
"""

from app.core.config import settings
from app.repositories.mock.branch_repository import MockBranchRepository
from app.repositories.mock.contribution_repository import MockContributionRepository
from app.repositories.mock.guarantor_repository import MockGuarantorRepository
from app.repositories.mock.loan_repository import MockLoanRepository
from app.repositories.mock.member_repository import MockMemberRepository
from app.repositories.mock.notification_repository import MockNotificationRepository
from app.repositories.mock.savings_repository import MockSavingsRepository
from app.repositories.mock.settings_repository import MockSettingsRepository
from app.repositories.mock.shares_repository import MockSharesRepository
from app.repositories.mock.transaction_repository import MockTransactionRepository
from app.repositories.mock.user_repository import MockUserRepository

_mock_user_repository = MockUserRepository()
_mock_member_repository = MockMemberRepository()
_mock_loan_repository = MockLoanRepository()
_mock_savings_repository = MockSavingsRepository()
_mock_shares_repository = MockSharesRepository()
_mock_guarantor_repository = MockGuarantorRepository()
_mock_contribution_repository = MockContributionRepository()
_mock_transaction_repository = MockTransactionRepository()
_mock_notification_repository = MockNotificationRepository()
_mock_settings_repository = MockSettingsRepository()
_mock_branch_repository = MockBranchRepository()


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


def get_transaction_repository() -> MockTransactionRepository:
    if settings.USE_MOCK_DATA:
        return _mock_transaction_repository
    raise NotImplementedError("Real TransactionRepository not implemented yet.")


def get_notification_repository() -> MockNotificationRepository:
    if settings.USE_MOCK_DATA:
        return _mock_notification_repository
    raise NotImplementedError("Real NotificationRepository not implemented yet.")


def get_settings_repository() -> MockSettingsRepository:
    if settings.USE_MOCK_DATA:
        return _mock_settings_repository
    raise NotImplementedError("Real SettingsRepository not implemented yet.")


def get_branch_repository() -> MockBranchRepository:
    if settings.USE_MOCK_DATA:
        return _mock_branch_repository
    raise NotImplementedError("Real BranchRepository not implemented yet.")
