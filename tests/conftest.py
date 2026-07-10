import os

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("USE_MOCK_DATA", "true")
os.environ.setdefault("ENVIRONMENT", "test")

import pytest
from httpx import ASGITransport, AsyncClient

from app.repositories.mock.guarantor_repository import reset_guarantor_data
from app.repositories.mock.loan_repository import reset_loan_data
from app.repositories.mock.member_repository import reset_member_data
from app.repositories.mock.savings_repository import reset_savings_data
from app.repositories.mock.shares_repository import reset_shares_data
from app.repositories.mock.user_repository import reset_user_data
from main import app


@pytest.fixture(autouse=True)
def reset_mock_data():
    reset_user_data()
    reset_member_data()
    reset_loan_data()
    reset_savings_data()
    reset_shares_data()
    reset_guarantor_data()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
