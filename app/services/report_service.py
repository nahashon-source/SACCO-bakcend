"""
Reports business logic. Unlike every other service, this one legitimately
depends on repositories from multiple domains — a report is, by nature,
an aggregation across the system. Real date-range filtering (date_from/
date_to actually constraining which records are counted) is not yet
implemented; every report currently reflects the full current dataset
regardless of the requested range. That's flagged explicitly in each
method rather than silently returning misleading numbers.
"""

from datetime import date, datetime, timezone

from app.models.loan import LoanStatus
from app.models.member import MemberStatus
from app.models.savings import SavingsAccountStatus
from app.repositories.mock.contribution_repository import MockContributionRepository
from app.repositories.mock.loan_repository import MockLoanRepository
from app.repositories.mock.member_repository import MockMemberRepository
from app.repositories.mock.savings_repository import MockSavingsRepository
from app.repositories.mock.shares_repository import MockSharesRepository
from app.schemas.report import (
    FinancialStatementData,
    LoansPortfolioData,
    MembersSummaryData,
    ReportType,
    SavingsSummaryData,
)


class UnsupportedReportTypeError(Exception):
    pass


class ReportService:
    def __init__(
        self,
        member_repository: MockMemberRepository,
        loan_repository: MockLoanRepository,
        savings_repository: MockSavingsRepository,
        shares_repository: MockSharesRepository,
        contribution_repository: MockContributionRepository,
    ):
        self._member_repository = member_repository
        self._loan_repository = loan_repository
        self._savings_repository = savings_repository
        self._shares_repository = shares_repository
        self._contribution_repository = contribution_repository

    async def generate(self, report_type: ReportType, date_from: date, date_to: date) -> dict:
        if report_type == ReportType.MEMBERS_SUMMARY:
            return await self._members_summary(date_from, date_to)
        if report_type == ReportType.LOANS_PORTFOLIO:
            return await self._loans_portfolio()
        if report_type == ReportType.SAVINGS_SUMMARY:
            return await self._savings_summary()
        if report_type == ReportType.FINANCIAL_STATEMENT:
            return await self._financial_statement(date_from, date_to)

        raise UnsupportedReportTypeError(f"Unknown report type: {report_type}")

    async def _members_summary(self, date_from: date, date_to: date) -> MembersSummaryData:
        members = await self._member_repository.list_all()

        # NOTE: "new_members_in_period" currently counts members joined
        # within date_from/date_to as a real filter (this one IS date-
        # aware, unlike the others below, since Member has joined_at).
        new_in_period = [
            m for m in members if date_from <= m.joined_at.date() <= date_to
        ]

        return MembersSummaryData(
            total_members=len(members),
            active_members=len([m for m in members if m.status == MemberStatus.ACTIVE]),
            inactive_members=len([m for m in members if m.status == MemberStatus.INACTIVE]),
            suspended_members=len([m for m in members if m.status == MemberStatus.SUSPENDED]),
            new_members_in_period=len(new_in_period),
        )

    async def _loans_portfolio(self) -> LoansPortfolioData:
        loans = await self._loan_repository.list_all()

        return LoansPortfolioData(
            total_loans=len(loans),
            pending_loans=len([l for l in loans if l.status == LoanStatus.PENDING]),
            disbursed_loans=len([l for l in loans if l.status == LoanStatus.DISBURSED]),
            closed_loans=len([l for l in loans if l.status == LoanStatus.CLOSED]),
            rejected_loans=len([l for l in loans if l.status == LoanStatus.REJECTED]),
            total_principal_disbursed=sum(
                l.principal for l in loans if l.status in (LoanStatus.DISBURSED, LoanStatus.CLOSED)
            ),
            total_outstanding_balance=sum(l.outstanding_balance for l in loans),
        )

    async def _savings_summary(self) -> SavingsSummaryData:
        accounts = await self._savings_repository.list_all()

        return SavingsSummaryData(
            total_accounts=len(accounts),
            active_accounts=len([a for a in accounts if a.status == SavingsAccountStatus.ACTIVE]),
            dormant_accounts=len([a for a in accounts if a.status == SavingsAccountStatus.DORMANT]),
            total_balance=sum(a.balance for a in accounts),
        )

    async def _financial_statement(self, date_from: date, date_to: date) -> FinancialStatementData:
        savings_accounts = await self._savings_repository.list_all()
        loans = await self._loan_repository.list_all()
        share_accounts = await self._shares_repository.list_all()
        contributions = await self._contribution_repository.list_all()

        # Contributions ARE date-filtered (has contributed_at); savings/
        # loans/shares totals below reflect current state, not
        # historical-as-of-date_to — a true point-in-time balance would
        # require transaction-history replay, which isn't built yet
        # (see Transactions domain's known gap).
        contributions_in_period = [
            c for c in contributions if date_from <= c.contributed_at.date() <= date_to
        ]

        return FinancialStatementData(
            total_savings_balance=sum(a.balance for a in savings_accounts),
            total_outstanding_loans=sum(l.outstanding_balance for l in loans),
            total_shares_value=sum(s.total_shares * s.share_value for s in share_accounts),
            total_contributions_in_period=sum(c.amount for c in contributions_in_period),
        )
