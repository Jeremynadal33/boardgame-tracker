from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from boardgame_tracker_backend.api.dependencies import (
    CurrentPlayerDep,
    OriginCheck,
    SessionDep,
    get_current_player,
)
from boardgame_tracker_backend.core.config import settings
from boardgame_tracker_backend.domain import players
from boardgame_tracker_backend.models.player import (
    PlayerCreate,
    PlayerPublic,
    PlayersPublic,
)

router = APIRouter(
    prefix="/players",
    tags=["players"],
)


###### Open endpoints ######
@router.post(
    "/signup",
    response_model=PlayerPublic,
    status_code=status.HTTP_201_CREATED,
    dependencies=[OriginCheck],
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


def _cookie_attributes() -> dict[str, Any]:
    # Shared by set_cookie and delete_cookie: they must match for the browser to clear it
    return {
        "key": settings.ACCESS_TOKEN_COOKIE_NAME,
        "httponly": True,
        "secure": settings.COOKIE_SECURE,
        "samesite": "strict",
    }


@router.post(
    "/login/access-token",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[OriginCheck],
)
def login_access_token(
    session: SessionDep,
    response: Response,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> None:
    """
    Log in: the access token is set in an HttpOnly cookie used for future requests
    """
    try:
        token = players.create_access_token(
            session=session, email=form_data.username, password=form_data.password
        )
        response.set_cookie(
            value=token.access_token,
            max_age=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
            **_cookie_attributes(),
        )
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


@router.post(
    "/logout", status_code=status.HTTP_204_NO_CONTENT, dependencies=[OriginCheck]
)
def logout(response: Response) -> None:
    """
    Log out: remove the access token cookie
    """
    response.delete_cookie(**_cookie_attributes())


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
