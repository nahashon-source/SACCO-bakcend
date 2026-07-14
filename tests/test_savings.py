import pytest

pytestmark = pytest.mark.asyncio


async def test_list_savings_accounts_returns_seeded_data(client):
    response = await client.get("/api/v1/savings")

    assert response.status_code == 200
    assert response.json()["data"]["totalItems"] == 9


async def test_deposit_increases_balance(client):
    response = await client.post("/api/v1/savings/1/deposit", json={"amount": 5000})

    assert response.status_code == 200
    assert response.json()["data"]["balance"] == 89500


async def test_withdraw_decreases_balance(client):
    response = await client.post(
        "/api/v1/savings/1/withdraw", json={"amount": 4500, "reason": "Emergency"}
    )

    assert response.status_code == 200
    assert response.json()["data"]["balance"] == 80000


async def test_withdraw_exceeding_balance_fails(client):
    response = await client.post(
        "/api/v1/savings/3/withdraw", json={"amount": 999999, "reason": "Too much"}
    )

    assert response.status_code == 400
    assert response.json()["success"] is False


async def test_withdraw_without_reason_fails_validation(client):
    response = await client.post("/api/v1/savings/1/withdraw", json={"amount": 100, "reason": "ab"})

    assert response.status_code == 422


async def test_deposit_to_nonexistent_account_returns_404(client):
    response = await client.post("/api/v1/savings/999/deposit", json={"amount": 100})

    assert response.status_code == 404


async def test_list_savings_filtered_by_branch(client):
    # Members 4,6,7 are in branch 2; savings accounts 4 and 6 belong to them
    response = await client.get("/api/v1/savings", params={"branch_id": 2})

    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert len(items) == 2
