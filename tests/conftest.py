import os

# Set required env vars BEFORE any app module is imported, since
# app.core.config.Settings validates at import time.
os.environ.setdefault("JWT_SECRET_KEY", "test-secret-key-not-for-production")
os.environ.setdefault("USE_MOCK_DATA", "true")
os.environ.setdefault("ENVIRONMENT", "test")

import pytest
from httpx import ASGITransport, AsyncClient

from main import app


@pytest.fixture
async def client():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
