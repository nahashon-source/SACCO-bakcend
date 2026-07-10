from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.repositories.factory import (
    get_guarantor_repository,
    get_loan_repository,
    get_member_repository,
)
from app.schemas.common import ApiResponse, PaginatedData
from app.schemas.guarantor import AddGuarantorRequest, GuarantorOut, GuarantorRespondRequest
from app.services.guarantor_service import (
    GuarantorAlreadyRespondedError,
    GuarantorNotFoundError,
    GuarantorService,
    LoanNotFoundForGuarantorError,
    MemberNotFoundForGuarantorError,
)

router = APIRouter(prefix="/guarantors", tags=["Guarantors"])


def get_guarantor_service() -> GuarantorService:
    return GuarantorService(
        guarantor_repository=get_guarantor_repository(),
        loan_repository=get_loan_repository(),
        member_repository=get_member_repository(),
    )


@router.get("", response_model=ApiResponse[PaginatedData[GuarantorOut]])
async def list_guarantors(
    loan_id: int | None = Query(default=None),
    member_id: int | None = Query(default=None),
    guarantor_service: GuarantorService = Depends(get_guarantor_service),
):
    guarantors = await guarantor_service.list_guarantors(loan_id, member_id)

    return ApiResponse(
        success=True,
        message="Guarantors retrieved",
        data=PaginatedData(
            items=[GuarantorOut.model_validate(g) for g in guarantors],
            page=1,
            page_size=len(guarantors) or 1,
            total_items=len(guarantors),
            total_pages=1,
        ),
    )


@router.post("", response_model=ApiResponse[GuarantorOut], status_code=status.HTTP_201_CREATED)
async def add_guarantor(
    payload: AddGuarantorRequest, guarantor_service: GuarantorService = Depends(get_guarantor_service)
):
    try:
        guarantor = await guarantor_service.add_guarantor(
            payload.loan_id, payload.member_id, payload.guaranteed_amount
        )
    except (LoanNotFoundForGuarantorError, MemberNotFoundForGuarantorError) as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return ApiResponse(success=True, message="Guarantor added", data=GuarantorOut.model_validate(guarantor))


@router.post("/{guarantor_id}/respond", response_model=ApiResponse[GuarantorOut])
async def respond_to_guarantor_request(
    guarantor_id: int,
    payload: GuarantorRespondRequest,
    guarantor_service: GuarantorService = Depends(get_guarantor_service),
):
    try:
        guarantor = await guarantor_service.respond(guarantor_id, payload.accept)
    except GuarantorNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except GuarantorAlreadyRespondedError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return ApiResponse(
        success=True, message="Response recorded", data=GuarantorOut.model_validate(guarantor)
    )
