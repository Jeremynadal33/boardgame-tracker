from fastapi import APIRouter, HTTPException, status
from boardgame_tracker_backend.api.dependencies import SessionDep, CurrentPlayerDep
from boardgame_tracker_backend.models.game import GameCreate, Game
from boardgame_tracker_backend.domain import games

from typing import Any, Sequence


router = APIRouter(
    prefix="/games",
    tags=["games"],
)


###### Open endpoints ######

@router.get("/", response_model=Sequence[Game], status_code=status.HTTP_200_OK)
def list_games(*, session: SessionDep) -> Sequence[Game]:
    """
    List all games.
    """

    return games.list_games(session=session)
###### Protected endpoints : Must use valid token ######

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_game(*, session: SessionDep, current_player: CurrentPlayerDep, game_in: GameCreate) -> Any:
    """
    Create new game.
    """

    try:
        db_game = games.create_game(session=session, current_player=current_player, game_in=game_in)
    except games.GameAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A game with the name '{e.name}' already exists",
        )
    except games.GameCreationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except games.GameValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An unexpected error occurred: {str(e)}",
        )

    return db_game