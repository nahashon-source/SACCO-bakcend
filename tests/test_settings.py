import pytest

pytestmark = pytest.mark.asyncio


async def test_get_settings_returns_seeded_data(client):
    response = await client.get("/api/v1/settings")

    assert response.status_code == 200
    assert response.json()["data"]["organizationName"] == "Freight in Time SACCO"


async def test_update_settings_partial_update_succeeds(client):
    response = await client.patch(
        "/api/v1/settings", json={"contactEmail": "new-contact@fitsacco.example.com"}
    )

    assert response.status_code == 200
    body = response.json()["data"]
    assert body["contactEmail"] == "new-contact@fitsacco.example.com"
    # Confirms partial update didn't wipe other fields
    assert body["organizationName"] == "Freight in Time SACCO"
