#! /usr/bin/env bash

## Will be replaced by docker compose entrypoint

set -e
set -x

bash ./scripts/prestart.sh

uv run fastapi dev boardgame_tracker_backend/main.py