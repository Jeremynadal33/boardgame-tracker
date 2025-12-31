from boardgame_tracker_backend.models.player import (
    Player,
    PlayerCreate,
    PlayerPublic,
    PlayersPublic,
    Token,
)
from boardgame_tracker_backend.core.security import get_password_hash, verify_password

from sqlmodel import Session, select, func
from sqlalchemy.exc import IntegrityError
from pydantic import ValidationError

from datetime import timedelta
from boardgame_tracker_backend.core.config import settings
from boardgame_tracker_backend.core import security


class PlayerAlreadyExistsError(Exception):
    def __init__(self, type: str, input: str):
        self.type = type
        self.input = input
        super().__init__(f"Player with {type} '{input}' already exists")


class PlayerNotFoundError(Exception):
    pass


class PlayerCreationError(Exception):
    pass


class PlayerValidationError(Exception):
    pass


class InvalidAccessTokenError(Exception):
    pass


class InactivePlayerError(Exception):
    pass


class InvalidCredentialsError(Exception):
    pass


class TokenCreationError(Exception):
    pass


def register_player(*, session: Session, player_in: PlayerCreate) -> Player:
    try:
        hashed_password = get_password_hash(player_in.password)

        db_player = Player.model_validate(
            player_in, update={"hashed_password": hashed_password}
        )
        session.add(db_player)
        session.commit()
        session.refresh(db_player)
        return db_player

    except IntegrityError as e:
        session.rollback()
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)

        if "UNIQUE constraint failed: player.email" in error_msg:
            raise PlayerAlreadyExistsError("email", player_in.email)
        elif "UNIQUE constraint failed: player.pseudo" in error_msg:
            raise PlayerAlreadyExistsError("pseudo", player_in.pseudo)
        else:
            raise PlayerCreationError(f"Unknown IntegrityError: {error_msg}")
    except ValidationError as e:
        session.rollback()
        raise PlayerValidationError(f"Player validation error: {str(e)}")
    except Exception as e:
        session.rollback()
        raise PlayerCreationError(f"Unknown error while creating player: {str(e)}")


def list_players(*, session: Session) -> PlayersPublic:
    count_statement = select(func.count()).select_from(Player)
    count = session.exec(count_statement).one()

    statement = select(Player)  # .offset(skip).limit(limit)
    players = session.exec(statement).all()

    return PlayersPublic(
        players=[PlayerPublic.model_validate(player) for player in players], count=count
    )


def get_player_by_email(*, session: Session, email: str) -> Player | None:
    statement = select(Player).where(Player.email == email)
    session_player = session.exec(statement).first()
    return session_player


# Should we raise specific errors here?
def authenticate(*, session: Session, email: str, password: str) -> Player:
    db_player = get_player_by_email(session=session, email=email)
    if not db_player:
        raise PlayerNotFoundError()
    if not verify_password(password, db_player.hashed_password):
        raise InvalidCredentialsError()
    return db_player


def create_access_token(*, session: Session, email: str, password: str) -> Token:
    try:
        player = authenticate(session=session, email=email, password=password)

        if not player.is_active:
            raise InactivePlayerError("Inactive player")

        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = security.create_access_token(
            subject=player.id, expires_delta=access_token_expires
        )
        return Token(access_token=access_token)
    except PlayerNotFoundError:
        raise PlayerNotFoundError(f"Player with email {email} not found")
    except InvalidCredentialsError:
        raise InvalidCredentialsError("Incorrect email or password")
    except InactivePlayerError:
        raise InactivePlayerError("Inactive player")
    except Exception as e:
        raise TokenCreationError(f"Failed to create access token: {str(e)}")
