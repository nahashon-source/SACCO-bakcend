from app.models.savings import SavingsAccount
from app.repositories.mock.savings_repository import MockSavingsRepository


class SavingsAccountNotFoundError(Exception):
    pass


class InsufficientBalanceError(Exception):
    pass


class SavingsService:
    def __init__(self, savings_repository: MockSavingsRepository):
        self._savings_repository = savings_repository

    async def list_accounts(self, member_id: int | None) -> list[SavingsAccount]:
        return await self._savings_repository.filter(member_id)

    async def get_account(self, account_id: int) -> SavingsAccount:
        account = await self._savings_repository.get_by_id(account_id)
        if account is None:
            raise SavingsAccountNotFoundError(f"Savings account {account_id} not found")
        return account

    async def deposit(self, account_id: int, amount: float) -> SavingsAccount:
        account = await self.get_account(account_id)
        new_balance = account.balance + amount
        return await self._savings_repository.update(account_id, {"balance": new_balance})

    async def withdraw(self, account_id: int, amount: float) -> SavingsAccount:
        account = await self.get_account(account_id)

        if amount > account.balance:
            raise InsufficientBalanceError(
                f"Withdrawal of {amount} exceeds available balance of {account.balance}"
            )

        new_balance = account.balance - amount
        return await self._savings_repository.update(account_id, {"balance": new_balance})
