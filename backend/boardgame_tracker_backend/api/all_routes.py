from fastapi import APIRouter

from boardgame_tracker_backend.api.routers import games, players

api_router = APIRouter()
api_router.include_router(games.router)
api_router.include_router(players.router)
