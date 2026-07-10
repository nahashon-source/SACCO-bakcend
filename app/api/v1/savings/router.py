from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.repositories.factory import get_savings_repository
from app.schemas.common import ApiResponse, PaginatedData
from app.schemas.savings import SavingsAccountOut, SavingsDepositRequest, SavingsWithdrawalRequest
from app.services.savings_service import (
    InsufficientBalanceError,
    SavingsAccountNotFoundError,
    SavingsService,
)

router = APIRouter(prefix="/savings", tags=["Savings"])


def get_savings_service() -> SavingsService:
    return SavingsService(savings_repository=get_savings_repository())


@router.get("", response_model=ApiResponse[PaginatedData[SavingsAccountOut]])
async def list_savings_accounts(
    member_id: int | None = Query(default=None),
    savings_service: SavingsService = Depends(get_savings_service),
):
    accounts = await savings_service.list_accounts(member_id)

    return ApiResponse(
        success=True,
        message="Savings accounts retrieved",
        data=PaginatedData(
            items=[SavingsAccountOut.model_validate(a) for a in accounts],
            page=1,
            page_size=len(accounts) or 1,
            total_items=len(accounts),
            total_pages=1,
        ),
    )


@router.get("/{account_id}", response_model=ApiResponse[SavingsAccountOut])
async def get_savings_account(
    account_id: int, savings_service: SavingsService = Depends(get_savings_service)
):
    try:
        account = await savings_service.get_account(account_id)
    except SavingsAccountNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return ApiResponse(
        success=True, message="Savings account retrieved", data=SavingsAccountOut.model_validate(account)
    )


@router.post("/{account_id}/deposit", response_model=ApiResponse[SavingsAccountOut])
async def deposit(
    account_id: int,
    payload: SavingsDepositRequest,
    savings_service: SavingsService = Depends(get_savings_service),
):
    try:
        account = await savings_service.deposit(account_id, payload.amount)
    except SavingsAccountNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc

    return ApiResponse(
        success=True, message="Deposit successful", data=SavingsAccountOut.model_validate(account)
    )


@router.post("/{account_id}/withdraw", response_model=ApiResponse[SavingsAccountOut])
async def withdraw(
    account_id: int,
    payload: SavingsWithdrawalRequest,
    savings_service: SavingsService = Depends(get_savings_service),
):
    try:
        account = await savings_service.withdraw(account_id, payload.amount)
    except SavingsAccountNotFoundError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc)) from exc
    except InsufficientBalanceError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    return ApiResponse(
        success=True, message="Withdrawal successful", data=SavingsAccountOut.model_validate(account)
    )
