from datetime import date
from enum import Enum

from app.schemas.base import CamelModel


class ReportType(str, Enum):
    MEMBERS_SUMMARY = "members_summary"
    LOANS_PORTFOLIO = "loans_portfolio"
    SAVINGS_SUMMARY = "savings_summary"
    FINANCIAL_STATEMENT = "financial_statement"


class MembersSummaryData(CamelModel):
    total_members: int
    active_members: int
    inactive_members: int
    suspended_members: int
    new_members_in_period: int


class LoansPortfolioData(CamelModel):
    total_loans: int
    pending_loans: int
    disbursed_loans: int
    closed_loans: int
    rejected_loans: int
    total_principal_disbursed: float
    total_outstanding_balance: float


class SavingsSummaryData(CamelModel):
    total_accounts: int
    active_accounts: int
    dormant_accounts: int
    total_balance: float


class FinancialStatementData(CamelModel):
    total_savings_balance: float
    total_outstanding_loans: float
    total_shares_value: float
    total_contributions_in_period: float


class ReportResultOut(CamelModel):
    type: ReportType
    generated_at: str
    date_from: date
    date_to: date
    data: MembersSummaryData | LoansPortfolioData | SavingsSummaryData | FinancialStatementData
