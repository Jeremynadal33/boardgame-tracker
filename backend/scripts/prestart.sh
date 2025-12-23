#! /usr/bin/env bash

set -e
set -x

# Let the DB start
uv run boardgame_tracker_backend/backend_prestart.py

# Run migrations for now, we just use create_all
# alembic upgrade head


# Create initial data in DB
uv run boardgame_tracker_backend/initial_data.py