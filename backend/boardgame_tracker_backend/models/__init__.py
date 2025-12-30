# Import all table models here so they can be imported together
from .game import Game
from .game_session import GameSession
from .player import Player

# Make all models available when importing from models package
__all__ = ["Game", "GameSession", "Player"]
