from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from sqlmodel import SQLModel, Field


### Represents a game session in the db
class GameSession(SQLModel, table=True):
    __table_name__ = "game_session"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    game_id: UUID = Field(foreign_key="game.id")
    played_at: datetime = Field(default_factory=datetime.utcnow)
    notes: Optional[str] = None
