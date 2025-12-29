from sqlmodel import Session
from pydantic import ValidationError
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

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
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/players/login/access-token"
)

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
    
    player = session.get(Player, token_data.sub)
    if not player:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Player not found")
    if not player.is_active:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Inactive player")
    return player


CurrentUser = Annotated[Player, Depends(get_current_player)]