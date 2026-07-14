import pytest

pytestmark = pytest.mark.asyncio


async def test_list_branches_returns_seeded_data(client):
    response = await client.get("/api/v1/branches")

    assert response.status_code == 200
    assert response.json()["data"]["totalItems"] == 3


async def test_get_branch_by_id_success(client):
    response = await client.get("/api/v1/branches/1")

    assert response.status_code == 200
    assert response.json()["data"]["code"] == "HQ"


async def test_get_nonexistent_branch_returns_404(client):
    response = await client.get("/api/v1/branches/999")

    assert response.status_code == 404


async def test_create_branch_succeeds(client):
    response = await client.post(
        "/api/v1/branches",
        json={"name": "Eldoret Branch", "code": "ELD", "address": "Uganda Road, Eldoret"},
    )

    assert response.status_code == 201
    assert response.json()["data"]["code"] == "ELD"


async def test_update_branch_status_succeeds(client):
    response = await client.patch("/api/v1/branches/2", json={"status": "inactive"})

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "inactive"


async def test_list_members_filtered_by_branch(client):
    response = await client.get("/api/v1/members", params={"branch_id": 1})

    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert all(m["branchId"] == 1 for m in items)
    assert len(items) == 6  # members 1,2,3,5,8,11 seeded to branch 1
