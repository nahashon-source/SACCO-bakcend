"""
In-memory Transaction repository. Currently read-only from the API's
perspective — no POST endpoint exists, since transactions should be a
byproduct of actions in other domains (a deposit creates a transaction
record), not something created directly by a client.

KNOWN GAP: Savings/Loans/Shares/Contributions services don't currently
call into this repository when they mutate balances — so the seeded
transactions here are illustrative demo data, not yet a live audit
trail of actual actions taken through the API. Wiring that up is a
cross-cutting change (every mutating service needs to also record a
transaction) better done as its own deliberate pass across all
services rather than bolted on inconsistently here.
"""

from datetime import datetime, timezone

from app.models.transaction import Transaction, TransactionStatus, TransactionType
from app.repositories.base import BaseRepository

_transactions: list[Transaction] = [
    Transaction(
        id=1,
        member_id=1,
        type=TransactionType.DEPOSIT,
        amount=5000,
        status=TransactionStatus.COMPLETED,
        reference="TXN-9001",
        created_at=datetime(2026, 6, 1, tzinfo=timezone.utc),
    ),
    Transaction(
        id=2,
        member_id=2,
        type=TransactionType.LOAN_DISBURSEMENT,
        amount=50000,
        status=TransactionStatus.COMPLETED,
        reference="TXN-9002",
        created_at=datetime(2025, 1, 15, tzinfo=timezone.utc),
    ),
    Transaction(
        id=3,
        member_id=1,
        type=TransactionType.CONTRIBUTION,
        amount=2000,
        status=TransactionStatus.COMPLETED,
        reference="TXN-9003",
        created_at=datetime(2026, 6, 1, tzinfo=timezone.utc),
    ),
]


class MockTransactionRepository(BaseRepository[Transaction]):
    async def get_by_id(self, entity_id: int) -> Transaction | None:
        return next((t for t in _transactions if t.id == entity_id), None)

    async def list_all(self) -> list[Transaction]:
        return _transactions

    async def filter(
        self,
        member_id: int | None,
        transaction_type: TransactionType | None,
        status: TransactionStatus | None,
    ) -> list[Transaction]:
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
    """Restore seed data. Called between tests for isolation."""
    global _transactions
    _transactions = list(_SEED_TRANSACTIONS)
