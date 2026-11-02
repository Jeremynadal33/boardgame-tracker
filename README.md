# Boardgame Tracker

A board game tracking application that allows you to record game scores, edit past game sessions, and create leagues for leaderboards. The app helps you determine which of your friends is the best board game player through competitive scoring and rankings.

Architecture, API security, deployment and open questions are documented in `docs/`, `backend/docs/` and `frontend/docs/` and published at <https://jeremynadal33.github.io/boardgame-tracker/>.

## Requirements

- [uv](https://docs.astral.sh/uv/) and Python 3.13 for the backend
- Node.js 24 and npm for the frontend
- Docker to build the image

## Run in development

SQLite is used as the database. The backend (port 8000) and the frontend (port 5173) run side by side; the frontend proxies `/api` to the backend.

```bash
# Backend: creates the tables and some dummy data, then starts fastapi in dev mode
cd backend
bash ./scripts/start.sh

# Frontend, in another terminal
cd frontend
npm install
npm run dev
```

Then open <http://localhost:5173>. In dev (`ENV=dev`, the default) the session cookie is not `Secure`, so plain http works.

### Getting a tunnel using ngrok

Make a tunnel running `ngrok http 8000`. Ngrok will print a forwarding URL (for example, `https://<random-subdomain>.ngrok-free.app`); use that URL as the base URL to access the API.

## Tests and checks

```bash
# Backend
cd backend
uv run pytest
uvx ruff check
uvx ruff format --check

# Frontend
cd frontend
npm run test:ci
npm run build   # also type-checks
```

## Run the production image

The image serves the API and the built frontend on port 8080. Outside `ENV=dev` a real `SECRET_KEY` is mandatory, and `COOKIE_SECURE` must be disabled when you reach the container over plain http.

```bash
docker build -t boardgame-tracker .
docker run --rm -p 8080:8080 \
  -e SECRET_KEY="$(openssl rand -hex 32)" \
  -e COOKIE_SECURE=false \
  -v boardgame-tracker-data:/data \
  boardgame-tracker
```

## Documentation

```bash
uv run --group docs mkdocs serve -a 127.0.0.1:8001   # live preview
uv run --group docs mkdocs build --strict
```
