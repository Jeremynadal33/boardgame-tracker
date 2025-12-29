from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from datetime import timedelta
from typing import Any

from boardgame_tracker_backend.api.dependencies import SessionDep

from boardgame_tracker_backend.models.player import PlayerCreate, PlayerPublic, PlayersPublic, Token
from boardgame_tracker_backend.domain import players

from boardgame_tracker_backend.core.config import settings
from boardgame_tracker_backend.core import security

router = APIRouter(
    prefix="/players",
    tags=["players"],
)

@router.post(
    "/signup"
    , response_model=PlayerPublic
)
def register_player(*, session: SessionDep, player_in: PlayerCreate) -> Any:
    """
    Create new player.
    """

    try:
        db_player = players.register_player(session=session, player_in=player_in)
    except players.PlayerAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"A player with the {e.type} '{e.input}' already exists"
        )
    except players.PlayerCreationError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred"
        )

    return db_player

@router.get(
    ""
    , response_model=PlayersPublic
)
def list_players(*, session: SessionDep) -> Any:
    """
    List all players.
    """
    # TODO: add error handling
    return players.list_players(session=session)


@router.post(
    "/login/access-token"
    , response_model=Token
)
def login_access_token(
    session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
) -> Token:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    try:
        token: Token = players.create_access_token(
            session=session, email=form_data.username, password=form_data.password
        )
        return token
    except players.PlayerNotFoundError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Player with email {form_data.username} not found")
    except players.InvalidCredentialsError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email or password")
    except players.TokenCreationError as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")