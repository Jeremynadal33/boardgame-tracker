from fastapi import APIRouter, HTTPException, status
from boardgame_tracker_backend.api.dependencies import SessionDep
from boardgame_tracker_backend.models.game import GameCreate, Game
from boardgame_tracker_backend.domain import games

from typing import Any


router = APIRouter(
    prefix="/games",
    tags=["games"],
)

@router.post(
    "/"
)
def create_game(*, session: SessionDep, game_in: GameCreate) -> Any:
    """
    Create new game.
    """

    # TODO : add created_by metadata in the Game model
    # TODO : get current user to add it to the metadata

    try:
        db_game = games.create_game(session=session, game_in=game_in)
    except games.GameAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A game with the name '{e.name}' already exists"
        )
    except games.GameCreationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

    return db_game

@router.get(
    "/"
)
def list_games(*, session: SessionDep) -> list[Game]:
    """
    List all games.
    """
    

    return games.list_games(session=session)