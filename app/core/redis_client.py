"""
Redis connection management. Redis is optional in this app: when
REDIS_URL is unset (local dev without Docker), get_redis() returns None
and every caller must handle that by skipping the Redis-dependent
behavior rather than crashing — see middleware/rate_limit.py for the
pattern to follow.
"""

import logging

import redis.asyncio as redis

from app.core.config import settings

logger = logging.getLogger(__name__)

_redis_client: redis.Redis | None = None
_connection_attempted = False


async def get_redis() -> redis.Redis | None:
    global _redis_client, _connection_attempted

    if not settings.REDIS_URL:
        return None

    if _redis_client is not None:
        return _redis_client

    if _connection_attempted:
        # Already failed once this process lifetime — don't retry on
        # every single request, that would add latency to every call
        # while Redis stays down. Log once, degrade gracefully instead.
        return None

    _connection_attempted = True

    try:
        client = redis.from_url(settings.REDIS_URL, decode_responses=True)
        await client.ping()
        _redis_client = client
        logger.info("Redis connection established.")
        return _redis_client
    except Exception as exc:
        logger.warning("Redis unavailable, continuing without it: %s", exc)
        return None
