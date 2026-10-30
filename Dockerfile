# syntax=docker/dockerfile:1

FROM node:24-alpine AS frontend
WORKDIR /frontend
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci
COPY frontend/ ./
RUN npm run build


FROM python:3.13-slim AS runtime
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app
COPY backend/pyproject.toml backend/uv.lock backend/README.md ./
RUN uv sync --frozen --no-dev --no-install-project
COPY backend/boardgame_tracker_backend ./boardgame_tracker_backend
RUN uv sync --frozen --no-dev

COPY --from=frontend /frontend/dist ./static

ENV PATH="/app/.venv/bin:$PATH" \
    ENV=prod \
    STATIC_DIR=/app/static \
    DATABASE_URL=sqlite:////data/boardgame_tracker.db
VOLUME /data
EXPOSE 8080

CMD ["sh", "-c", "python -m boardgame_tracker_backend.initial_data && exec fastapi run boardgame_tracker_backend/main.py --port 8080"]
