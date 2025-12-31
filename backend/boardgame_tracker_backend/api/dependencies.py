from sqlmodel import Session
from pydantic import ValidationError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError
from uuid import UUID

from collections.abc import Generator

from typing import Annotated

from boardgame_tracker_backend.core.database import engine
from boardgame_tracker_backend.core.config import settings
from boardgame_tracker_backend.core import security

from boardgame_tracker_backend.models.player import Player, TokenPayload


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]

# Not entirely sure about why TokenDep is needed but it looks like best practice
# The tokenUrl is the endpoint where clients can get the token
# Must match the actual login endpoint in boardgame_tracker_backend/api/routers/players.py
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=settings.LOGIN_ENDPOINT)

TokenDep = Annotated[str, Depends(reusable_oauth2)]


def get_current_player(session: SessionDep, token: TokenDep) -> Player:
    try:
        payload = security.decode_access_token(token)

        token_data = TokenPayload(**payload)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
        )
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    # Convert string UUID back to UUID object for database query
    try:
        player_id = UUID(token_data.sub) if token_data.sub else None
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    if not player_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    player = session.get(Player, player_id)
    if not player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Player not found"
        )
    if not player.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Inactive player"
        )
    return player


CurrentPlayerDep = Annotated[Player, Depends(get_current_player)]
