import pytest

pytestmark = pytest.mark.asyncio


async def test_list_contributions_returns_seeded_data(client):
    response = await client.get("/api/v1/contributions")

    assert response.status_code == 200
    assert response.json()["data"]["totalItems"] == 3


async def test_list_contributions_filtered_by_member(client):
    response = await client.get("/api/v1/contributions", params={"member_id": 1})

    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert len(items) == 2
    assert all(c["memberId"] == 1 for c in items)


async def test_list_contributions_filtered_by_type(client):
    response = await client.get("/api/v1/contributions", params={"type": "welfare"})

    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert len(items) == 1
    assert items[0]["type"] == "welfare"


async def test_record_contribution_with_valid_member_succeeds(client):
    response = await client.post(
        "/api/v1/contributions",
        json={"memberId": 2, "type": "special", "amount": 1000},
    )

    assert response.status_code == 201
    assert response.json()["data"]["amount"] == 1000


async def test_record_contribution_with_nonexistent_member_fails(client):
    response = await client.post(
        "/api/v1/contributions",
        json={"memberId": 999, "type": "monthly", "amount": 1000},
    )

    assert response.status_code == 400
