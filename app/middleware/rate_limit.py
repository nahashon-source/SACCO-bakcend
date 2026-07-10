"""
Rate limiting middleware. Fixed-window counter per client IP, backed by
Redis. Fails open (allows the request through) if Redis is unreachable —
a rate limiter that takes the whole API down during a Redis outage would
be a worse outcome than temporarily allowing unrestricted traffic. This
trade-off should be revisited if abuse/DoS resistance becomes a higher
priority than uptime during infra incidents.
"""

import logging

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse

from app.core.config import settings
from app.core.redis_client import get_redis

logger = logging.getLogger(__name__)


class RateLimitMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        redis_client = await get_redis()

        # No Redis configured/reachable — skip enforcement entirely.
        if redis_client is None:
            return await call_next(request)

        client_ip = request.client.host if request.client else "unknown"
        key = f"rate_limit:{client_ip}:{request.url.path}"

        try:
            current = await redis_client.incr(key)
            if current == 1:
                await redis_client.expire(key, 60)

            if current > settings.RATE_LIMIT_PER_MINUTE:
                return JSONResponse(
                    status_code=429,
                    content={
                        "success": False,
                        "message": "Too many requests. Please try again shortly.",
                        "data": None,
                        "errors": ["rate_limit_exceeded"],
                    },
                )
        except Exception as exc:
            # Redis errored mid-request (connection dropped, etc.) — same
            # fail-open policy as above, logged for visibility.
            logger.warning("Rate limit check failed, allowing request: %s", exc)

        return await call_next(request)
