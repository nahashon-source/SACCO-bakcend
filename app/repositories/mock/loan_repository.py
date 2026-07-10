"""
In-memory Loan repository. Seed data mirrors the frontend's
src/mocks/data.ts fixtures for consistency across both mock layers.
"""

from datetime import datetime, timezone

from app.models.loan import Loan, LoanStatus
from app.repositories.base import BaseRepository

_loans: list[Loan] = [
    Loan(
        id=1,
        loan_number="LN-2001",
        member_id=1,
        principal=100000,
        interest_rate=12,
        term_months=12,
        outstanding_balance=75000,
        status=LoanStatus.DISBURSED,
        applied_at=datetime(2025, 1, 10, tzinfo=timezone.utc),
        disbursed_at=datetime(2025, 1, 15, tzinfo=timezone.utc),
        created_at=datetime(2025, 1, 10, tzinfo=timezone.utc),
        updated_at=datetime(2025, 1, 15, tzinfo=timezone.utc),
    ),
    Loan(
        id=2,
        loan_number="LN-2002",
        member_id=2,
        principal=50000,
        interest_rate=12,
        term_months=6,
        outstanding_balance=50000,
        status=LoanStatus.PENDING,
        applied_at=datetime(2026, 6, 20, tzinfo=timezone.utc),
        disbursed_at=None,
        created_at=datetime(2026, 6, 20, tzinfo=timezone.utc),
        updated_at=datetime(2026, 6, 20, tzinfo=timezone.utc),
    ),
    Loan(
        id=3,
        loan_number="LN-2003",
        member_id=4,
        principal=200000,
        interest_rate=14,
        term_months=24,
        outstanding_balance=200000,
        status=LoanStatus.PENDING,
        applied_at=datetime(2026, 7, 1, tzinfo=timezone.utc),
        disbursed_at=None,
        created_at=datetime(2026, 7, 1, tzinfo=timezone.utc),
        updated_at=datetime(2026, 7, 1, tzinfo=timezone.utc),
    ),
]

_next_id = 4


class MockLoanRepository(BaseRepository[Loan]):
    async def get_by_id(self, entity_id: int) -> Loan | None:
        return next((l for l in _loans if l.id == entity_id), None)

    async def list_all(self) -> list[Loan]:
        return _loans

    async def filter(
        self, member_id: int | None, status: LoanStatus | None
    ) -> list[Loan]:
        results = _loans

        if member_id is not None:
            results = [l for l in results if l.member_id == member_id]

        if status is not None:
            results = [l for l in results if l.status == status]

        return results

    async def create(self, entity: Loan) -> Loan:
        global _next_id
        entity = entity.model_copy(update={"id": _next_id})
        _next_id += 1
        _loans.append(entity)
        return entity

    async def update(self, entity_id: int, updates: dict) -> Loan | None:
        loan = await self.get_by_id(entity_id)
        if loan is None:
            return None
        updated = loan.model_copy(
            update={**updates, "updated_at": datetime.now(timezone.utc)}
        )
        _loans[_loans.index(loan)] = updated
        return updated

    async def delete(self, entity_id: int) -> bool:
        loan = await self.get_by_id(entity_id)
        if loan is None:
            return False
        _loans.remove(loan)
        return True


_SEED_LOANS = list(_loans)


def reset_loan_data() -> None:
    """Restore seed data. Called between tests for isolation — see tests/conftest.py."""
    global _loans, _next_id
    _loans = list(_SEED_LOANS)
    _next_id = 4
