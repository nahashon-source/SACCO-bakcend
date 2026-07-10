from datetime import datetime, timezone

from app.models.guarantor import Guarantor, GuarantorStatus
from app.repositories.mock.guarantor_repository import MockGuarantorRepository
from app.repositories.mock.loan_repository import MockLoanRepository
from app.repositories.mock.member_repository import MockMemberRepository


class GuarantorNotFoundError(Exception):
    pass


class LoanNotFoundForGuarantorError(Exception):
    pass


class MemberNotFoundForGuarantorError(Exception):
    pass


class GuarantorAlreadyRespondedError(Exception):
    pass


class GuarantorService:
    def __init__(
        self,
        guarantor_repository: MockGuarantorRepository,
        loan_repository: MockLoanRepository,
        member_repository: MockMemberRepository,
    ):
        self._guarantor_repository = guarantor_repository
        self._loan_repository = loan_repository
        self._member_repository = member_repository

    async def list_guarantors(self, loan_id: int | None, member_id: int | None) -> list[Guarantor]:
        return await self._guarantor_repository.filter(loan_id, member_id)

    async def add_guarantor(self, loan_id: int, member_id: int, guaranteed_amount: float) -> Guarantor:
        loan = await self._loan_repository.get_by_id(loan_id)
        if loan is None:
            raise LoanNotFoundForGuarantorError(f"Loan with id {loan_id} does not exist")

        member = await self._member_repository.get_by_id(member_id)
        if member is None:
            raise MemberNotFoundForGuarantorError(f"Member with id {member_id} does not exist")

        now = datetime.now(timezone.utc)
        new_guarantor = Guarantor(
            id=0,  # overwritten by repository
            loan_id=loan_id,
            member_id=member_id,
            guaranteed_amount=guaranteed_amount,
            status=GuarantorStatus.PENDING,
            responded_at=None,
            created_at=now,
            updated_at=now,
        )
        return await self._guarantor_repository.create(new_guarantor)

    async def respond(self, guarantor_id: int, accept: bool) -> Guarantor:
        guarantor = await self._guarantor_repository.get_by_id(guarantor_id)
        if guarantor is None:
            raise GuarantorNotFoundError(f"Guarantor request {guarantor_id} not found")

        if guarantor.status != GuarantorStatus.PENDING:
            raise GuarantorAlreadyRespondedError(
                f"This guarantor request has already been responded to (status: {guarantor.status.value})"
            )

        new_status = GuarantorStatus.ACCEPTED if accept else GuarantorStatus.DECLINED
        updated = await self._guarantor_repository.update(
            guarantor_id, {"status": new_status, "responded_at": datetime.now(timezone.utc)}
        )
        return updated
