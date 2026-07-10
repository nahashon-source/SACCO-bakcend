from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.api.v1.auth.router import router as auth_router
from app.api.v1.contributions.router import router as contributions_router
from app.api.v1.guarantors.router import router as guarantors_router
from app.api.v1.loans.router import router as loans_router
from app.api.v1.members.router import router as members_router
from app.api.v1.notifications.router import router as notifications_router
from app.api.v1.reports.router import router as reports_router
from app.api.v1.savings.router import router as savings_router
from app.api.v1.settings.router import router as settings_router
from app.api.v1.shares.router import router as shares_router
from app.api.v1.transactions.router import router as transactions_router
from app.core.config import settings
from app.core.logging import configure_logging
from app.middleware.rate_limit import RateLimitMiddleware

configure_logging()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_middleware(RateLimitMiddleware)


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "success": False,
            "message": exc.detail,
            "data": None,
            "errors": [exc.detail],
        },
    )


app.include_router(auth_router, prefix=settings.API_V1_PREFIX)
app.include_router(members_router, prefix=settings.API_V1_PREFIX)
app.include_router(loans_router, prefix=settings.API_V1_PREFIX)
app.include_router(savings_router, prefix=settings.API_V1_PREFIX)
app.include_router(shares_router, prefix=settings.API_V1_PREFIX)
app.include_router(guarantors_router, prefix=settings.API_V1_PREFIX)
app.include_router(contributions_router, prefix=settings.API_V1_PREFIX)
app.include_router(transactions_router, prefix=settings.API_V1_PREFIX)
app.include_router(notifications_router, prefix=settings.API_V1_PREFIX)
app.include_router(settings_router, prefix=settings.API_V1_PREFIX)
app.include_router(reports_router, prefix=settings.API_V1_PREFIX)


@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok", "mock_data": settings.USE_MOCK_DATA}
