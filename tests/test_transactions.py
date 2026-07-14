import pytest

pytestmark = pytest.mark.asyncio


async def test_list_transactions_returns_seeded_data(client):
    response = await client.get("/api/v1/transactions")

    assert response.status_code == 200
    assert response.json()["data"]["totalItems"] == 10


async def test_list_transactions_filtered_by_member(client):
    response = await client.get("/api/v1/transactions", params={"member_id": 1})

    assert response.status_code == 200
    assert len(response.json()["data"]["items"]) == 2


async def test_list_transactions_filtered_by_type(client):
    response = await client.get("/api/v1/transactions", params={"type": "loan_disbursement"})

    assert response.status_code == 200
    items = response.json()["data"]["items"]
    # TXN-9002 (member 2) and TXN-9004 (member 6) are both loan_disbursement
    assert len(items) == 2
    references = {item["reference"] for item in items}
    assert references == {"TXN-9002", "TXN-9004"}


async def test_get_transaction_by_id_success(client):
    response = await client.get("/api/v1/transactions/1")

    assert response.status_code == 200
    assert response.json()["data"]["reference"] == "TXN-9001"


async def test_get_nonexistent_transaction_returns_404(client):
    response = await client.get("/api/v1/transactions/999")

    assert response.status_code == 404
