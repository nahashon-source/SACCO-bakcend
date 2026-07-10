import pytest

pytestmark = pytest.mark.asyncio

VALID_CREDENTIALS = {"email": "staff@fitsacco.example.com", "password": "Password123!"}


async def test_login_with_correct_credentials_succeeds(client):
    response = await client.post("/api/v1/auth/login", json=VALID_CREDENTIALS)

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert "access_token" in body["data"]["tokens"]
    assert body["data"]["user"]["email"] == VALID_CREDENTIALS["email"]


async def test_login_with_wrong_password_fails(client):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": VALID_CREDENTIALS["email"], "password": "wrong-password"},
    )

    assert response.status_code == 401
    assert response.json()["success"] is False


async def test_login_with_unknown_email_fails(client):
    response = await client.post(
        "/api/v1/auth/login",
        json={"email": "nobody@example.com", "password": "whatever"},
    )

    assert response.status_code == 401


async def test_get_me_without_token_returns_401(client):
    response = await client.get("/api/v1/auth/me")

    assert response.status_code == 401


async def test_get_me_with_valid_token_returns_user(client):
    login_response = await client.post("/api/v1/auth/login", json=VALID_CREDENTIALS)
    access_token = login_response.json()["data"]["tokens"]["access_token"]

    response = await client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {access_token}"},
    )

    assert response.status_code == 200
    assert response.json()["data"]["email"] == VALID_CREDENTIALS["email"]


async def test_refresh_token_issues_new_access_token(client):
    login_response = await client.post("/api/v1/auth/login", json=VALID_CREDENTIALS)
    refresh_token = login_response.json()["data"]["tokens"]["refresh_token"]

    response = await client.post(
        "/api/v1/auth/refresh", json={"refresh_token": refresh_token}
    )

    assert response.status_code == 200
    assert "access_token" in response.json()["data"]
