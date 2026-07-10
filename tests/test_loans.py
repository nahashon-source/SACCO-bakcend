import pytest

pytestmark = pytest.mark.asyncio


async def test_list_loans_returns_seeded_data(client):
    response = await client.get("/api/v1/loans")

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["totalItems"] == 3


async def test_apply_for_loan_with_valid_member_succeeds(client):
    response = await client.post(
        "/api/v1/loans",
        json={"memberId": 1, "principal": 30000, "termMonths": 6, "purpose": "Business expansion"},
    )

    assert response.status_code == 201
    body = response.json()
    assert body["data"]["status"] == "pending"
    assert body["data"]["outstandingBalance"] == 30000


async def test_apply_for_loan_with_nonexistent_member_fails(client):
    response = await client.post(
        "/api/v1/loans",
        json={"memberId": 999, "principal": 30000, "termMonths": 6, "purpose": "Business expansion"},
    )

    assert response.status_code == 400
    assert response.json()["success"] is False


async def test_approve_pending_loan_succeeds(client):
    response = await client.post("/api/v1/loans/2/approve")

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "approved"


async def test_approve_already_approved_loan_fails(client):
    await client.post("/api/v1/loans/3/approve")
    response = await client.post("/api/v1/loans/3/approve")

    assert response.status_code == 409


async def test_reject_loan_requires_reason(client):
    response = await client.post("/api/v1/loans/2/reject", json={"reason": "no"})

    # "no" is under the 5-char minimum — Pydantic validation should reject it
    assert response.status_code == 422


async def test_reject_pending_loan_with_valid_reason_succeeds(client):
    response = await client.post(
        "/api/v1/loans/2/reject", json={"reason": "Insufficient collateral provided"}
    )

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "rejected"


async def test_repay_non_disbursed_loan_fails(client):
    # Loan 2 is pending, not disbursed
    response = await client.post("/api/v1/loans/2/repay", json={"amount": 1000})

    assert response.status_code == 409


async def test_repay_disbursed_loan_reduces_balance(client):
    # Loan 1 is seeded as disbursed with outstandingBalance 75000
    response = await client.post("/api/v1/loans/1/repay", json={"amount": 25000})

    assert response.status_code == 200
    assert response.json()["data"]["outstandingBalance"] == 50000
