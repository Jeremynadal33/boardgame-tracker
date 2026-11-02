from pathlib import Path

from fastapi import FastAPI

from boardgame_tracker_backend.api.all_routes import api_router
from boardgame_tracker_backend.core.config import settings
from boardgame_tracker_backend.frontend import mount_frontend


app = FastAPI(
    title=settings.PROJECT_NAME,
    # openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(api_router, prefix=settings.API_V1_STR)


# Must stay after every other route: it catches everything else
if settings.STATIC_DIR:
    mount_frontend(app, Path(settings.STATIC_DIR), settings.API_V1_STR)
else:

    @app.get("/")
    def home():
        return {"message": "Welcome to the Boardgame Tracker API!"}


def square(n):
    return n * n
