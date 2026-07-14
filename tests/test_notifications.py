import pytest

pytestmark = pytest.mark.asyncio


async def test_list_notifications_returns_seeded_data(client):
    response = await client.get("/api/v1/notifications")

    assert response.status_code == 200
    assert response.json()["data"]["totalItems"] == 5


async def test_list_unread_notifications_filters_correctly(client):
    response = await client.get("/api/v1/notifications", params={"is_read": False})

    assert response.status_code == 200
    items = response.json()["data"]["items"]
    # Notifications 1, 3, 5 are seeded unread
    assert len(items) == 3
    assert all(n["isRead"] is False for n in items)


async def test_mark_notification_as_read_succeeds(client):
    response = await client.patch("/api/v1/notifications/1/read")

    assert response.status_code == 200
    assert response.json()["data"]["isRead"] is True


async def test_mark_nonexistent_notification_as_read_returns_404(client):
    response = await client.patch("/api/v1/notifications/999/read")

    assert response.status_code == 404


async def test_mark_all_notifications_as_read(client):
    response = await client.patch("/api/v1/notifications/read-all")
    assert response.status_code == 200

    list_response = await client.get("/api/v1/notifications", params={"is_read": False})
    assert len(list_response.json()["data"]["items"]) == 0
