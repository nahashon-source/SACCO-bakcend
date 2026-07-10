from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.repositories.factory import (
    get_contribution_repository,
    get_loan_repository,
    get_member_repository,
    get_savings_repository,
    get_shares_repository,
)
from app.schemas.common import ApiResponse
from app.schemas.report import ReportResultOut, ReportType
from app.services.report_service import ReportService, UnsupportedReportTypeError

router = APIRouter(prefix="/reports", tags=["Reports"])


def get_report_service() -> ReportService:
    return ReportService(
        member_repository=get_member_repository(),
        loan_repository=get_loan_repository(),
        savings_repository=get_savings_repository(),
        shares_repository=get_shares_repository(),
        contribution_repository=get_contribution_repository(),
    )


@router.get("", response_model=ApiResponse[ReportResultOut])
async def generate_report(
    type: ReportType = Query(...),
    date_from: date = Query(...),
    date_to: date = Query(...),
    report_service: ReportService = Depends(get_report_service),
):
    if date_from > date_to:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="date_from must not be after date_to",
        )

    try:
        data = await report_service.generate(type, date_from, date_to)
    except UnsupportedReportTypeError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc)) from exc

    from datetime import datetime, timezone

    return ApiResponse(
        success=True,
        message="Report generated",
        data=ReportResultOut(
            type=type,
            generated_at=datetime.now(timezone.utc).isoformat(),
            date_from=date_from,
            date_to=date_to,
            data=data,
        ),
    )
