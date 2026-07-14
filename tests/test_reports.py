import pytest

pytestmark = pytest.mark.asyncio


async def test_members_summary_report(client):
    response = await client.get(
        "/api/v1/reports",
        params={"type": "members_summary", "date_from": "2024-01-01", "date_to": "2026-12-31"},
    )

    assert response.status_code == 200
    data = response.json()["data"]["data"]
    assert data["totalMembers"] == 12
    assert data["activeMembers"] == 9


async def test_loans_portfolio_report(client):
    response = await client.get(
        "/api/v1/reports",
        params={"type": "loans_portfolio", "date_from": "2024-01-01", "date_to": "2026-12-31"},
    )

    assert response.status_code == 200
    data = response.json()["data"]["data"]
    assert data["totalLoans"] == 7
    assert data["pendingLoans"] == 2


async def test_savings_summary_report(client):
    response = await client.get(
        "/api/v1/reports",
        params={"type": "savings_summary", "date_from": "2024-01-01", "date_to": "2026-12-31"},
    )

    assert response.status_code == 200
    data = response.json()["data"]["data"]
    assert data["totalAccounts"] == 9
    assert data["totalBalance"] == 873600


async def test_financial_statement_report(client):
    response = await client.get(
        "/api/v1/reports",
        params={"type": "financial_statement", "date_from": "2024-01-01", "date_to": "2026-12-31"},
    )

    assert response.status_code == 200
    data = response.json()["data"]["data"]
    assert "totalSavingsBalance" in data
    assert "totalSharesValue" in data


async def test_invalid_date_range_fails(client):
    response = await client.get(
        "/api/v1/reports",
        params={"type": "members_summary", "date_from": "2026-12-31", "date_to": "2024-01-01"},
    )

    assert response.status_code == 400
