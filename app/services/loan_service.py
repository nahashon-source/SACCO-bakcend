"""
Loan business logic. Enforces status transition rules and cross-domain
validation (member must exist) that don't belong in either repository.
"""

from datetime import datetime, timezone

from app.models.loan import Loan, LoanStatus
from app.repositories.mock.loan_repository import MockLoanRepository
from app.repositories.mock.member_repository import MockMemberRepository


class LoanNotFoundError(Exception):
    pass


class MemberNotFoundForLoanError(Exception):
    pass


class InvalidLoanStatusTransitionError(Exception):
    pass


class LoanService:
    def __init__(self, loan_repository: MockLoanRepository, member_repository: MockMemberRepository):
        self._loan_repository = loan_repository
        self._member_repository = member_repository

    async def list_loans(
        self, member_id: int | None, status: LoanStatus | None
    ) -> list[Loan]:
        return await self._loan_repository.filter(member_id, status)

    async def get_loan(self, loan_id: int) -> Loan:
        loan = await self._loan_repository.get_by_id(loan_id)
        if loan is None:
            raise LoanNotFoundError(f"Loan with id {loan_id} not found")
        return loan

    async def apply(
        self, member_id: int, principal: float, term_months: int
    ) -> Loan:
        member = await self._member_repository.get_by_id(member_id)
        if member is None:
            raise MemberNotFoundForLoanError(f"Member with id {member_id} does not exist")

        existing_loans = await self._loan_repository.list_all()
        loan_number = f"LN-{2000 + len(existing_loans) + 1}"

        now = datetime.now(timezone.utc)
        new_loan = Loan(
            id=0,  # overwritten by repository
            loan_number=loan_number,
            member_id=member_id,
            principal=principal,
            interest_rate=12.0,  # flat rate for now — real rate config is a Settings-domain concern, not built yet
            term_months=term_months,
            outstanding_balance=principal,
            status=LoanStatus.PENDING,
            applied_at=now,
            disbursed_at=None,
            created_at=now,
            updated_at=now,
        )

        return await self._loan_repository.create(new_loan)

    async def approve(self, loan_id: int) -> Loan:
        loan = await self.get_loan(loan_id)

        if loan.status != LoanStatus.PENDING:
            raise InvalidLoanStatusTransitionError(
                f"Cannot approve a loan with status '{loan.status.value}' — only pending loans can be approved."
            )

        updated = await self._loan_repository.update(loan_id, {"status": LoanStatus.APPROVED})
        return updated

    async def reject(self, loan_id: int, reason: str) -> Loan:
        loan = await self.get_loan(loan_id)

        if loan.status != LoanStatus.PENDING:
            raise InvalidLoanStatusTransitionError(
                f"Cannot reject a loan with status '{loan.status.value}' — only pending loans can be rejected."
            )

        updated = await self._loan_repository.update(
            loan_id, {"status": LoanStatus.REJECTED, "rejection_reason": reason}
        )
        return updated

    async def repay(self, loan_id: int, amount: float) -> Loan:
        loan = await self.get_loan(loan_id)

        if loan.status not in (LoanStatus.DISBURSED,):
            raise InvalidLoanStatusTransitionError(
                f"Cannot record a repayment against a loan with status '{loan.status.value}' — loan must be disbursed first."
            )

        new_balance = max(0.0, loan.outstanding_balance - amount)
        new_status = LoanStatus.CLOSED if new_balance == 0 else loan.status

        updated = await self._loan_repository.update(
            loan_id, {"outstanding_balance": new_balance, "status": new_status}
        )
        return updated
