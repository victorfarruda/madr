FROM python:3.12-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/uv

COPY . /app
WORKDIR /app

RUN uv venv && uv sync --frozen

EXPOSE 8000
CMD uv run uvicorn --host 0.0.0.0 madr.app:app