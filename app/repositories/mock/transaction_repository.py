"""
In-memory Transaction repository. See original docstring note: not yet
wired as a live audit trail of other services' mutations — this is
still illustrative seed data, just more of it now.
"""

from datetime import datetime, timezone

from app.models.transaction import Transaction, TransactionStatus, TransactionType
from app.repositories.base import BaseRepository


def _d(y, m, d):
    return datetime(y, m, d, tzinfo=timezone.utc)


_transactions: list[Transaction] = [
    Transaction(id=1, member_id=1, type=TransactionType.DEPOSIT, amount=5000, status=TransactionStatus.COMPLETED, reference="TXN-9001", created_at=_d(2026, 6, 1)),
    Transaction(id=2, member_id=2, type=TransactionType.LOAN_DISBURSEMENT, amount=50000, status=TransactionStatus.COMPLETED, reference="TXN-9002", created_at=_d(2025, 1, 15)),
    Transaction(id=3, member_id=1, type=TransactionType.CONTRIBUTION, amount=2000, status=TransactionStatus.COMPLETED, reference="TXN-9003", created_at=_d(2026, 6, 1)),
    Transaction(id=4, member_id=6, type=TransactionType.LOAN_DISBURSEMENT, amount=150000, status=TransactionStatus.COMPLETED, reference="TXN-9004", created_at=_d(2025, 11, 18)),
    Transaction(id=5, member_id=6, type=TransactionType.LOAN_REPAYMENT, amount=30000, status=TransactionStatus.COMPLETED, reference="TXN-9005", created_at=_d(2026, 5, 1)),
    Transaction(id=6, member_id=8, type=TransactionType.DEPOSIT, amount=10000, status=TransactionStatus.COMPLETED, reference="TXN-9006", created_at=_d(2026, 6, 5)),
    Transaction(id=7, member_id=2, type=TransactionType.SHARE_PURCHASE, amount=20000, status=TransactionStatus.COMPLETED, reference="TXN-9007", created_at=_d(2024, 6, 10)),
    Transaction(id=8, member_id=9, type=TransactionType.WITHDRAWAL, amount=3000, status=TransactionStatus.COMPLETED, reference="TXN-9008", created_at=_d(2026, 6, 25)),
    Transaction(id=9, member_id=4, type=TransactionType.CONTRIBUTION, amount=1500, status=TransactionStatus.COMPLETED, reference="TXN-9009", created_at=_d(2026, 5, 3)),
    Transaction(id=10, member_id=5, type=TransactionType.LOAN_REPAYMENT, amount=35000, status=TransactionStatus.COMPLETED, reference="TXN-9010", created_at=_d(2025, 9, 5)),
]


class MockTransactionRepository(BaseRepository[Transaction]):
    async def get_by_id(self, entity_id: int) -> Transaction | None:
        return next((t for t in _transactions if t.id == entity_id), None)

    async def list_all(self) -> list[Transaction]:
        return _transactions

    async def filter(self, member_id: int | None, transaction_type: TransactionType | None, status: TransactionStatus | None) -> list[Transaction]:
        results = _transactions
        if member_id is not None:
            results = [t for t in results if t.member_id == member_id]
        if transaction_type is not None:
            results = [t for t in results if t.type == transaction_type]
        if status is not None:
            results = [t for t in results if t.status == status]
        return results

    async def create(self, entity: Transaction) -> Transaction:
        _transactions.append(entity)
        return entity

    async def update(self, entity_id: int, updates: dict) -> Transaction | None:
        raise NotImplementedError("Transactions are immutable once created.")

    async def delete(self, entity_id: int) -> bool:
        raise NotImplementedError("Transactions cannot be deleted — use status=reversed instead.")


_SEED_TRANSACTIONS = list(_transactions)


def reset_transaction_data() -> None:
    global _transactions
    _transactions = list(_SEED_TRANSACTIONS)
