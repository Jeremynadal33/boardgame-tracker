from sqlmodel import Session, select
from sqlalchemy.exc import IntegrityError
from typing import Sequence

from boardgame_tracker_backend.models.game import Game, GameCreate

# Define domain-specific exceptions

class GameAlreadyExistsError(Exception):
    def __init__(self, name: str):
        self.name = name
        super().__init__(f"Game with name '{name}' already exists")

class GameCreationError(Exception):
    pass


def create_game(*, session: Session, game_in: GameCreate) -> Game:

    try:
        db_game = Game.model_validate(game_in)
        session.add(db_game)
        session.commit()
        session.refresh(db_game)
        return db_game
    except IntegrityError as e:
        session.rollback()
        error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
        
        if "UNIQUE constraint failed: game.name" in error_msg:
            raise GameAlreadyExistsError(game_in.name)
        else:
            raise GameCreationError(f"Failed to create game: {error_msg}")




def list_games(*, session: Session) -> Sequence[Game]:
    games = session.exec(select(Game)).all()
    return games