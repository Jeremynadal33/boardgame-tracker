from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from typing import Any

from boardgame_tracker_backend.api.dependencies import (
    SessionDep,
    CurrentPlayerDep,
    get_current_player,
)

from boardgame_tracker_backend.models.player import (
    PlayerCreate,
    PlayerPublic,
    PlayersPublic,
    Token,
)
from boardgame_tracker_backend.domain import players


router = APIRouter(
    prefix="/players",
    tags=["players"],
)


###### Open endpoints ######
@router.post(
    "/signup", response_model=PlayerPublic, status_code=status.HTTP_201_CREATED
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
            detail=f"A player with the {e.type} '{e.input}' already exists",
        )
    except players.PlayerCreationError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )

    return db_player


@router.post(
    "/login/access-token", response_model=Token, status_code=status.HTTP_200_OK
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
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Player with email {form_data.username} not found",
        )
    except players.InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    except players.TokenCreationError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


###### Protected endpoints : Must use valid token ######
@router.get("/me", response_model=PlayerPublic, status_code=status.HTTP_200_OK)
def read_current_player(current_player: CurrentPlayerDep) -> Any:
    """
    Get current player.
    """
    return current_player


@router.get(
    "",
    response_model=PlayersPublic,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_current_player)],
)
def list_players(*, session: SessionDep) -> Any:
    """
    List all players.
    """
    # TODO: add error handling
    return players.list_players(session=session)
