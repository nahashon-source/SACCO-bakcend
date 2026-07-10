from app.models.transaction import Transaction, TransactionStatus, TransactionType
from app.repositories.mock.transaction_repository import MockTransactionRepository


class TransactionNotFoundError(Exception):
    pass


class TransactionService:
    def __init__(self, transaction_repository: MockTransactionRepository):
        self._transaction_repository = transaction_repository

    async def list_transactions(
        self,
        member_id: int | None,
        transaction_type: TransactionType | None,
        status: TransactionStatus | None,
    ) -> list[Transaction]:
        return await self._transaction_repository.filter(member_id, transaction_type, status)

    async def get_transaction(self, transaction_id: int) -> Transaction:
        transaction = await self._transaction_repository.get_by_id(transaction_id)
        if transaction is None:
            raise TransactionNotFoundError(f"Transaction {transaction_id} not found")
        return transaction
