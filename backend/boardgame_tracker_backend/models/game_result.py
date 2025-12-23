from typing import Optional, Dict, Any
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, JSON, Column


### Represents a game result in the db
class GameResult(SQLModel, table=True):
    __table_name__ = "game_result"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    session_id: UUID = Field(foreign_key="game_session.id")
    player_id: UUID = Field(foreign_key="player.id")
    position: int = Field(ge=1)  # Position in the game (1st, 2nd, etc.)
    score: int = Field(default=0)
    additional_game_stats: Optional[Dict[str, Any]] = Field(
        default=None, sa_column=Column(JSON)
    )
