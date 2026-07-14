import pytest

pytestmark = pytest.mark.asyncio


async def test_list_members_returns_seeded_data(client):
    response = await client.get("/api/v1/members")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["totalItems"] == 4
    assert len(body["data"]["items"]) == 4
    assert "pageSize" in body["data"]  # confirms camelCase serialization


async def test_list_members_search_filters_results(client):
    response = await client.get("/api/v1/members", params={"search": "Wanjiru"})

    assert response.status_code == 200
    items = response.json()["data"]["items"]
    assert len(items) == 1
    assert items[0]["fullName"] == "Wanjiru Kamau"


async def test_get_member_by_id_success(client):
    response = await client.get("/api/v1/members/1")

    assert response.status_code == 200
    assert response.json()["data"]["memberNumber"] == "MEM-0001"


async def test_get_member_not_found_returns_404(client):
    response = await client.get("/api/v1/members/999")

    assert response.status_code == 404


async def test_create_member_success(client):
    response = await client.post(
        "/api/v1/members",
        json={
            "fullName": "Test Member",
            "email": "test.member@example.com",
            "phoneNumber": "+254700000000",
        },
    )

    assert response.status_code == 201
    body = response.json()
    assert body["data"]["fullName"] == "Test Member"
    assert body["data"]["memberNumber"].startswith("MEM-")


async def test_update_member_success(client):
    response = await client.patch("/api/v1/members/2", json={"status": "inactive"})

    assert response.status_code == 200
    assert response.json()["data"]["status"] == "inactive"


async def test_delete_nonexistent_member_returns_404(client):
    response = await client.delete("/api/v1/members/999")

    assert response.status_code == 404
