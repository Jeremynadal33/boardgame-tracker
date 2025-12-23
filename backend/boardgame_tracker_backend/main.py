from fastapi import FastAPI

from boardgame_tracker_backend.api.all_routes import api_router
from boardgame_tracker_backend.core.config import settings


app = FastAPI(
    title=settings.PROJECT_NAME,
    # openapi_url=f"{settings.API_V1_STR}/openapi.json",
    # generate_unique_id_function=custom_generate_unique_id,
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def home():
    return {"message": "Welcome to the Boardgame Tracker API!"}

def square(n):
    return n * n