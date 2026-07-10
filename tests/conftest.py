import os

os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("USE_MOCK_DATA", "true")
os.environ.setdefault("ENVIRONMENT", "test")

import pytest
from httpx import ASGITransport, AsyncClient

from app.repositories.mock.loan_repository import reset_loan_data
from app.repositories.mock.member_repository import reset_member_data
from app.repositories.mock.user_repository import reset_user_data
from main import app


@pytest.fixture(autouse=True)
def reset_mock_data():
    """
    Runs before every test automatically. Mock repositories use
    module-level state that persists across the whole test session —
    without this reset, tests become order-dependent (a test that
    changes a loan's status can silently break a later test expecting
    the original seeded state). Add a reset_<domain>_data() call here
    for every new mock repository going forward.
    """
    reset_user_data()
    reset_member_data()
    reset_loan_data()
    yield


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
