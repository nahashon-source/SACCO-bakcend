from app.models.savings import SavingsAccount
from app.repositories.mock.member_repository import MockMemberRepository
from app.repositories.mock.savings_repository import MockSavingsRepository


class SavingsAccountNotFoundError(Exception):
    pass


class InsufficientBalanceError(Exception):
    pass


class SavingsService:
    def __init__(
        self, savings_repository: MockSavingsRepository, member_repository: MockMemberRepository
    ):
        self._savings_repository = savings_repository
        self._member_repository = member_repository

    async def list_accounts(
        self, member_id: int | None, branch_id: int | None = None
    ) -> list[SavingsAccount]:
        accounts = await self._savings_repository.filter(member_id)

        if branch_id is not None:
            # Same derivation approach as Loans: SavingsAccount has no
            # branch_id of its own, it's derived from the account
            # holder's current Member.branch_id.
            members = await self._member_repository.list_all()
            member_ids_in_branch = {m.id for m in members if m.branch_id == branch_id}
            accounts = [a for a in accounts if a.member_id in member_ids_in_branch]

        return accounts

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
