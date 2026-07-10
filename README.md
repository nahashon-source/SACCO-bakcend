# SACCO Management System — Backend

A production-ready FastAPI backend for a SACCO (Savings and Credit Cooperative) management system, designed to be consumed by a separately-developed React 19 + TypeScript frontend. Built with a layered architecture (API → Service → Repository → Data) so the current in-memory mock data layer can be swapped for real PostgreSQL persistence without touching business logic or routes.

---

## Tech Stack

- **Python 3.12** (pinned — 3.14 lacks prebuilt wheels for `asyncpg`/`pydantic-core` as of this writing)
- **FastAPI** — web framework
- **Pydantic v2** — validation and settings
- **SQLAlchemy 2.0 (async)** + **Alembic** — ORM and migrations (wired in once real persistence replaces mocks)
- **python-jose** + **passlib[argon2]** — JWT auth, password hashing
- **Redis** — rate limiting, caching, Celery broker (optional — app degrades gracefully without it)
- **Celery** — background jobs (not yet wired)
- **Docker** + **Docker Compose** — containerization
- **Pytest** — testing
- **Ruff** + **Black** — linting and formatting
- **Gunicorn** + **Uvicorn workers** — production server

---

## Architecture

```
API Layer (routes)
    ↓
Service Layer (business logic)
    ↓
Repository Layer (data access — mock or real, same interface)
    ↓
Data (in-memory mock, or PostgreSQL once wired)
```

**Rules enforced throughout:**

- Business logic never lives in route files — routes only validate input, call a service, and wrap the response.
- Repositories only do data access — no business rules.
- Every repository (mock or real) implements the same abstract interface (`app/repositories/base.py`), so services never know which one they're talking to.

---

## Project Structure

```
backend/
├── app/
│   ├── api/v1/              # One folder per domain: auth, members, savings, ...
│   ├── core/                 # config.py, security.py, logging.py, redis_client.py
│   ├── models/                # Domain entities (storage-agnostic Pydantic models)
│   ├── schemas/               # Request/response DTOs (never expose internal fields like hashed_password)
│   ├── services/               # Business logic
│   ├── repositories/
│   │   ├── base.py            # Abstract interface
│   │   ├── mock/               # In-memory implementations (active now)
│   │   └── factory.py          # USE_MOCK_DATA switch point
│   ├── dependencies/           # FastAPI dependencies (e.g. get_current_user)
│   ├── middleware/             # rate_limit.py
│   └── workers/                # Celery tasks (not yet wired)
├── tests/
├── migrations/                 # Alembic (not yet generated — no real DB yet)
├── .github/workflows/ci.yml
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── main.py
└── .env.example
```

### Domain module pattern

Every domain (once built) follows this shape, matching `auth`:

```
app/models/<domain>.py          # Entity
app/schemas/<domain>.py          # DTOs
app/repositories/mock/<domain>_repository.py
app/repositories/factory.py      # add get_<domain>_repository()
app/services/<domain>_service.py
app/api/v1/<domain>/router.py
```

**Implemented so far:** `auth` (login, refresh, me, logout).
**Pending:** `members`, `savings`, `shares`, `loans`, `guarantors`, `contributions`, `transactions`, `reports`, `notifications`, `settings`.

---

## Getting Started

### 1. Python version

This project requires **Python 3.12** specifically:

```bash
py -3.12 -m venv venv
source venv/Scripts/activate   # Windows Git Bash
pip install -r requirements.txt
```

### 2. Environment variables

```bash
cp .env.example .env
```

| Variable               | Required                      | Description                                                                                      |
| ---------------------- | ----------------------------- | ------------------------------------------------------------------------------------------------ |
| `JWT_SECRET_KEY`       | Yes                           | Long random string. Generate with `python -c "import secrets; print(secrets.token_urlsafe(64))"` |
| `USE_MOCK_DATA`        | No (default `true`)           | `true` = in-memory mock repositories, `false` = real PostgreSQL (not yet implemented)            |
| `DATABASE_URL`         | Only if `USE_MOCK_DATA=false` | PostgreSQL connection string                                                                     |
| `REDIS_URL`            | No                            | Enables rate limiting/caching when set. App runs fine without it.                                |
| `CORS_ALLOWED_ORIGINS` | No (default `localhost:5173`) | JSON array of allowed frontend origins                                                           |

### 3. Run

**Without Docker:**

```bash
uvicorn main:app --reload --port 8000
```

**With Docker (includes Redis):**

```bash
docker compose up --build
```

Visit `http://localhost:8000/docs` for interactive Swagger UI.

### 4. Test credentials (mock data)

```
email: staff@fitsacco.example.com
password: Password123!
```

---

## Mock Data Layer

Since real PostgreSQL persistence isn't built yet, `USE_MOCK_DATA=true` (the default) routes all repository calls to in-memory Python data structures, seeded with demo data. This lets the full API — and the frontend consuming it — function end-to-end today.

**Switching to real data later:** implement a `Real<Domain>Repository` per domain matching `app/repositories/base.py`'s interface, add the `else` branch in `app/repositories/factory.py`, set `USE_MOCK_DATA=false` and `DATABASE_URL`. No service or route code changes.

---

## API Response Contract

Every endpoint returns:

```json
{
  "success": true,
  "message": "Operation completed successfully",
  "data": {},
  "errors": null
}
```

This matches the frontend's `ApiResponse<T>` type exactly.

---

## Redis & Rate Limiting

Redis is **optional** in this app by design:

- If `REDIS_URL` is unset or Redis is unreachable, rate limiting silently no-ops (fails open) — the API keeps working, just without request throttling.
- Once `REDIS_URL` is set (via Docker locally, or a managed Redis add-on on Render), rate limiting activates automatically — 60 requests/minute per IP per route by default (`RATE_LIMIT_PER_MINUTE` setting).

**Known trade-off:** failing open means a Redis outage won't take down the API, but also means rate limiting isn't enforced during that outage. This favors uptime over strict abuse prevention — revisit if DoS resistance becomes a higher priority.

---

## Testing

```bash
pytest -v
```

Current coverage: health check, login (success/wrong password/unknown email), protected route with/without token, token refresh. Test suite forces `USE_MOCK_DATA=true` and a test-only JWT secret — never depends on your local `.env`.

---

## CI/CD

`.github/workflows/ci.yml` runs on every push/PR to `main` (scoped to `backend/**` changes only):

1. Ruff lint check
2. Black format check
3. Pytest suite

**Assumes repo layout:** `backend/` and `frontend/` as sibling folders in the same repository. If your actual layout differs, the workflow's `working-directory` and `paths` filter need adjusting.

---

## Deployment (Render) — Planned, Not Yet Done

Target setup:

- Render Web Service, Docker-based (uses the existing `Dockerfile`)
- Managed Redis add-on for `REDIS_URL`
- Environment variables set in Render's dashboard (never committed)
- `USE_MOCK_DATA=true` initially, flipped to `false` once real PostgreSQL persistence is built and a Render PostgreSQL instance is provisioned

Full step-by-step deployment instructions to be added once this is executed.

---

## Known Limitations / Pending Work

| Item                                                | Status                                                                                                                   |
| --------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| Real PostgreSQL repositories                        | Not started — mock data only                                                                                             |
| Alembic migrations                                  | Not started (no schema to migrate yet)                                                                                   |
| Domains beyond `auth`                               | Not started (members, savings, shares, loans, guarantors, contributions, transactions, reports, notifications, settings) |
| Celery background jobs                              | Not wired                                                                                                                |
| Docker tested locally                               | Not yet — Docker Desktop not installed on dev machine                                                                    |
| Render deployment                                   | Not yet executed                                                                                                         |
| Password reset / email verification                 | Not started                                                                                                              |
| Object storage (Cloudinary/S3) for document uploads | Not started                                                                                                              |

---

## Commit Convention

```
<type>: <short description>

[optional body]
```

Types: `feat`, `fix`, `refactor`, `chore`, `test`, `ci`
