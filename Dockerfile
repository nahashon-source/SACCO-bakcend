FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Install dependencies first — this layer only rebuilds when
# requirements.txt changes, not on every source code edit.
COPY requirements.txt .
RUN pip install -r requirements.txt

# Now copy application code.
COPY . .

EXPOSE 8000

# Gunicorn manages Uvicorn worker processes for production.
# Worker count: start conservative (2), tune based on actual load/CPU
# once deployed — this is a starting point, not a measured value.
CMD ["gunicorn", "main:app", \
     "--workers", "2", \
     "--worker-class", "uvicorn.workers.UvicornWorker", \
     "--bind", "0.0.0.0:8000", \
     "--timeout", "60"]
