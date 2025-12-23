from fastapi import APIRouter

from boardgame_tracker_backend.api.routers import games

api_router = APIRouter()
api_router.include_router(games.router)
