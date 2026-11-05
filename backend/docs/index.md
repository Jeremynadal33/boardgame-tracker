# Backend

FastAPI api based backend for Boardgame Tracker.

Greatly inspired by [full-stack-fastapi-template](https://github.com/fastapi/full-stack-fastapi-template/tree/3826039f51d0eafef01b5e814bd35e0c582b0104).

## Project structure

```ini
backend/
├── pyproject.toml
├── uv.lock
├── scripts/
│   ├── prestart.sh # Waits for the DB, creates the tables and the initial data
│   └── start.sh # Dev entrypoint: prestart then fastapi dev
├── boardgame_tracker_backend/
│   ├── main.py # Instanciate the actual app
│   ├── frontend.py # Serves the built frontend (single page app) when STATIC_DIR is set
│   ├── backend_prestart.py # Checks the DB is reachable
│   ├── initial_data.py # Creates the tables (and dummy data in dev)
│   ├── api/ # Contains API routing and dependency management
│   │   ├── all_routes.py # Aggregates all routes for easier import in main app
│   │   ├── dependencies.py # What is use in many APIs (db session, current player, origin check)
│   │   └── routers/ # Declare all routes but are passthrough to domain functions
│   │       ├── game_sessions.py
│   │       ├── games.py
│   │       └── players.py
│   ├── core/
│   │   ├── config.py # All config, env, env vars, ...
│   │   ├── database.py # Create the SQLAlchemy engine
│   │   └── security.py # Password hashing and JWT
│   ├── domain/ # The actual logic (what does it mean to create a user ?, ...)
│   │   ├── games.py
│   │   └── players.py
│   └── models/ # ORM models + corresponding "pydantic" schemas
│       ├── game.py
│       ├── game_result.py
│       ├── game_session.py
│       └── player.py
└── tests/
    └── boardgame_tracker_backend/ # Mirrors the package layout
```

## Layers

- **Routers** (`api/routers`) only translate HTTP to domain calls and domain errors to HTTP status codes.
- **Domain** (`domain/`) holds the rules and raises its own exceptions (`GameAlreadyExistsError`, ...).
- **Models** (`models/`) are the SQLModel tables and the pydantic schemas (`*Create`, `*Public`).

## Serving the frontend

When `STATIC_DIR` is set, `frontend.py` mounts `/assets` and answers every other `GET` with `index.html` so that the React router can handle the URL. The whole `/api` namespace is reserved: an unknown route under it answers `404` for every method instead of falling back to the app.
