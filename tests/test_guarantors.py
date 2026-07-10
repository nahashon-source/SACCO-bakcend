import pytest

pytestmark = pytest.mark.asyncio


async def test_list_guarantors_returns_seeded_data(client):
    response = await client.get("/api/v1/guarantors")

    assert response.status_code == 200
    assert response.json()["data"]["totalItems"] == 2


async def test_add_guarantor_with_valid_loan_and_member_succeeds(client):
    response = await client.post(
        "/api/v1/guarantors",
        json={"loanId": 3, "memberId": 1, "guaranteedAmount": 50000},
    )

    assert response.status_code == 201
    assert response.json()["data"]["status"] == "pending"


async def test_add_guarantor_with_nonexistent_loan_fails(client):
    response = await client.post(
        "/api/v1/guarantors",
        json={"loanId": 999, "memberId": 1, "guaranteedAmount": 50000},
    )

    assert response.status_code == 400


async def test_add_guarantor_with_nonexistent_member_fails(client):
    response = await client.post(
        "/api/v1/guarantors",
        json={"loanId": 1, "memberId": 999, "guaranteedAmount": 50000},
    )

    assert response.status_code == 400


async def test_accept_pending_guarantor_request_succeeds(client):
    response = await client.post("/api/v1/guarantors/2/respond", json={"accept": True})

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "accepted"


async def test_decline_pending_guarantor_request_succeeds(client):
    response = await client.post("/api/v1/guarantors/2/respond", json={"accept": False})

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "declined"


async def test_respond_to_already_answered_request_fails(client):
    # Guarantor 1 is already seeded as "accepted"
    response = await client.post("/api/v1/guarantors/1/respond", json={"accept": False})

    assert response.status_code == 409
