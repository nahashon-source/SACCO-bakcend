from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.models.loan import LoanStatus
from app.repositories.factory import get_loan_repository, get_member_repository
from app.schemas.common import ApiResponse, PaginatedData
from app.schemas.loan import LoanApplicationRequest, LoanOut, LoanRejectRequest, LoanRepaymentRequest
from app.services.loan_service import (
    InvalidLoanStatusTransitionError,
    LoanNotFoundError,
    LoanService,
    MemberNotFoundForLoanError,
)

router = APIRouter(prefix="/loans", tags=["Loans"])


def get_loan_service() -> LoanService:
    return LoanService(
        loan_repository=get_loan_repository(),
        member_repository=get_member_repository(),
    )


@router.get("", response_model=ApiResponse[PaginatedData[LoanOut]])
async def list_loans(
    member_id: int | None = Query(default=None),
    status_filter: LoanStatus | None = Query(default=None, alias="status"),
    branch_id: int | None = Query(default=None),
    loan_service: LoanService = Depends(get_loan_service),
):
    loans = await loan_service.list_loans(member_id, status_filter, branch_id)

    return ApiResponse(
        success=True,
        message="Loans retrieved",
        data=PaginatedData(
            items=[LoanOut.model_validate(l) for l in loans],
            page=1,
            page_size=len(loans) or 1,
            total_items=len(loans),
            total_pages=1,
        ),
    )


@router.get("/{loan_id}", response_model=ApiResponse[LoanOut])
async def get_loan(loan_id: int, loan_service: LoanService = Depends(get_loan_service)):
    try:
        loan = await loan_service.get_loan(loan_id)
    except LoanNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return ApiResponse(success=True, message="Loan retrieved", data=LoanOut.model_validate(loan))


@router.post("", response_model=ApiResponse[LoanOut], status_code=status.HTTP_201_CREATED)
async def apply_for_loan(
    payload: LoanApplicationRequest, loan_service: LoanService = Depends(get_loan_service)
):
    try:
        loan = await loan_service.apply(payload.member_id, payload.principal, payload.term_months)
    except MemberNotFoundForLoanError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return ApiResponse(success=True, message="Loan application submitted", data=LoanOut.model_validate(loan))


@router.post("/{loan_id}/approve", response_model=ApiResponse[LoanOut])
async def approve_loan(loan_id: int, loan_service: LoanService = Depends(get_loan_service)):
    try:
        loan = await loan_service.approve(loan_id)
    except LoanNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidLoanStatusTransitionError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return ApiResponse(success=True, message="Loan approved", data=LoanOut.model_validate(loan))


@router.post("/{loan_id}/reject", response_model=ApiResponse[LoanOut])
async def reject_loan(
    loan_id: int, payload: LoanRejectRequest, loan_service: LoanService = Depends(get_loan_service)
):
    try:
        loan = await loan_service.reject(loan_id, payload.reason)
    except LoanNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidLoanStatusTransitionError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return ApiResponse(success=True, message="Loan rejected", data=LoanOut.model_validate(loan))


@router.post("/{loan_id}/disburse", response_model=ApiResponse[LoanOut])
async def disburse_loan(loan_id: int, loan_service: LoanService = Depends(get_loan_service)):
    try:
        loan = await loan_service.disburse(loan_id)
    except LoanNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidLoanStatusTransitionError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return ApiResponse(success=True, message="Loan disbursed", data=LoanOut.model_validate(loan))


@router.post("/{loan_id}/repay", response_model=ApiResponse[LoanOut])
async def repay_loan(
    loan_id: int, payload: LoanRepaymentRequest, loan_service: LoanService = Depends(get_loan_service)
):
    try:
        loan = await loan_service.repay(loan_id, payload.amount)
    except LoanNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InvalidLoanStatusTransitionError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc)) from exc

    return ApiResponse(success=True, message="Repayment recorded", data=LoanOut.model_validate(loan))
