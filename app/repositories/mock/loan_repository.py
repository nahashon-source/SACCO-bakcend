from datetime import datetime, timezone

from app.models.loan import Loan, LoanStatus
from app.repositories.base import BaseRepository


def _d(y, m, d):
    return datetime(y, m, d, tzinfo=timezone.utc)


_loans: list[Loan] = [
    Loan(id=1, loan_number="LN-2001", member_id=1, principal=100000, interest_rate=12, term_months=12, outstanding_balance=75000, status=LoanStatus.DISBURSED, applied_at=_d(2025, 1, 10), disbursed_at=_d(2025, 1, 15), created_at=_d(2025, 1, 10), updated_at=_d(2025, 1, 15)),
    Loan(id=2, loan_number="LN-2002", member_id=2, principal=50000, interest_rate=12, term_months=6, outstanding_balance=50000, status=LoanStatus.PENDING, applied_at=_d(2026, 6, 20), disbursed_at=None, created_at=_d(2026, 6, 20), updated_at=_d(2026, 6, 20)),
    Loan(id=3, loan_number="LN-2003", member_id=4, principal=200000, interest_rate=14, term_months=24, outstanding_balance=200000, status=LoanStatus.PENDING, applied_at=_d(2026, 7, 1), disbursed_at=None, created_at=_d(2026, 7, 1), updated_at=_d(2026, 7, 1)),
    Loan(id=4, loan_number="LN-2004", member_id=5, principal=35000, interest_rate=12, term_months=6, outstanding_balance=0, status=LoanStatus.CLOSED, applied_at=_d(2025, 3, 1), disbursed_at=_d(2025, 3, 5), created_at=_d(2025, 3, 1), updated_at=_d(2025, 9, 5)),
    Loan(id=5, loan_number="LN-2005", member_id=6, principal=150000, interest_rate=13, term_months=18, outstanding_balance=120000, status=LoanStatus.DISBURSED, applied_at=_d(2025, 11, 12), disbursed_at=_d(2025, 11, 18), created_at=_d(2025, 11, 12), updated_at=_d(2026, 5, 1)),
    Loan(id=6, loan_number="LN-2006", member_id=8, principal=80000, interest_rate=12, term_months=12, outstanding_balance=80000, status=LoanStatus.APPROVED, applied_at=_d(2026, 6, 28), disbursed_at=None, created_at=_d(2026, 6, 28), updated_at=_d(2026, 7, 2)),
    Loan(id=7, loan_number="LN-2007", member_id=9, principal=20000, interest_rate=12, term_months=4, outstanding_balance=20000, status=LoanStatus.REJECTED, applied_at=_d(2026, 5, 10), disbursed_at=None, created_at=_d(2026, 5, 10), updated_at=_d(2026, 5, 14)),
]

_next_id = 8


class MockLoanRepository(BaseRepository[Loan]):
    async def get_by_id(self, entity_id: int) -> Loan | None:
        return next((l for l in _loans if l.id == entity_id), None)

    async def list_all(self) -> list[Loan]:
        return _loans

    async def filter(self, member_id: int | None, status: LoanStatus | None) -> list[Loan]:
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
        updated = loan.model_copy(update={**updates, "updated_at": datetime.now(timezone.utc)})
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
    global _loans, _next_id
    _loans = list(_SEED_LOANS)
    _next_id = 8
