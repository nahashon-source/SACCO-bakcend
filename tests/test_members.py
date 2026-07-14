import pytest

pytestmark = pytest.mark.asyncio


async def test_list_members_returns_seeded_data(client):
    response = await client.get("/api/v1/members")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["totalItems"] == 12
    assert len(body["data"]["items"]) == 12
    assert "pageSize" in body["data"]


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


async def test_get_member_includes_kyc_and_optional_fields(client):
    response = await client.get("/api/v1/members/1")

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["kycStatus"] == "verified"
    assert body["nextOfKin"]["fullName"] == "James Kamau"
    assert body["employment"]["employerName"] == "Freight in Time Ltd"
    assert len(body["documents"]) == 1


async def test_get_member_with_no_optional_data_returns_nulls(client):
    response = await client.get("/api/v1/members/2")

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["nextOfKin"] is None
    assert body["employment"] is None
    assert body["documents"] == []


async def test_update_next_of_kin_succeeds(client):
    response = await client.put(
        "/api/v1/members/2/next-of-kin",
        json={"fullName": "Mary Odhiambo", "relationship": "Mother", "phoneNumber": "+254712345999"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["nextOfKin"]["fullName"] == "Mary Odhiambo"


async def test_update_employment_succeeds(client):
    response = await client.put(
        "/api/v1/members/2/employment",
        json={"employerName": "Test Corp", "jobTitle": "Analyst", "monthlyIncome": 60000},
    )

    assert response.status_code == 200
    assert response.json()["data"]["employment"]["monthlyIncome"] == 60000


async def test_update_next_of_kin_for_nonexistent_member_fails(client):
    response = await client.put(
        "/api/v1/members/999/next-of-kin",
        json={"fullName": "Nobody", "relationship": "N/A", "phoneNumber": "+254700000000"},
    )

    assert response.status_code == 404
