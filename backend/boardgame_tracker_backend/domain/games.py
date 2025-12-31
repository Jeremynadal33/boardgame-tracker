from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from typing import Sequence

from boardgame_tracker_backend.models.game import Game, GameCreate
from boardgame_tracker_backend.models.player import Player

from pydantic import ValidationError

# Define domain-specific exceptions


class GameAlreadyExistsError(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Game with name '{name}' already exists")


class GameCreationError(Exception):
    pass


class GameValidationError(Exception):
    pass


def create_game(*, session: Session, current_player: Player, game_in: GameCreate) -> Game:
    try:

        db_game = Game.model_validate(game_in, update={"created_by": current_player.id})
        session.add(db_game)
        session.commit()
        session.refresh(db_game)
        return db_game
    except IntegrityError as e:
        session.rollback()
        error_msg = str(e.orig) if hasattr(e, "orig") else str(e)

        if "UNIQUE constraint failed: game.name" in error_msg:
            raise GameAlreadyExistsError(game_in.name)
        else:
            raise GameCreationError(f"Unknown IntegrityError: {error_msg}")
    except ValidationError as e:
        session.rollback()
        raise GameValidationError(f"Game validation error: {str(e)}")
    except Exception as e:
        session.rollback()
        raise GameCreationError(f"Failed to create game: {str(e)}")


def list_games(*, session: Session) -> Sequence[Game]:
    games = session.exec(select(Game)).all()
    return games
