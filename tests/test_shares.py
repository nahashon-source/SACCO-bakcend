import pytest

pytestmark = pytest.mark.asyncio


async def test_list_share_accounts_returns_seeded_data(client):
    response = await client.get("/api/v1/shares")

    assert response.status_code == 200
    body = response.json()
    assert body["data"]["totalItems"] == 6
    assert body["data"]["items"][0]["totalValue"] == 500 * 100


async def test_purchase_shares_for_new_member_creates_account(client):
    response = await client.post(
        "/api/v1/shares/purchase", json={"memberId": 3, "numberOfShares": 200}
    )

    assert response.status_code == 201
    assert response.json()["data"]["totalShares"] == 200


async def test_purchase_shares_for_existing_holder_accumulates(client):
    response = await client.post(
        "/api/v1/shares/purchase", json={"memberId": 1, "numberOfShares": 100}
    )

    assert response.status_code == 201
    assert response.json()["data"]["totalShares"] == 600


async def test_purchase_shares_for_nonexistent_member_fails(client):
    response = await client.post(
        "/api/v1/shares/purchase", json={"memberId": 999, "numberOfShares": 100}
    )

    assert response.status_code == 400
