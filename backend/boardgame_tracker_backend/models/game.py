from typing import Optional
from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field

from boardgame_tracker_backend.core.config import settings

class GameBase(SQLModel):
    name: str = Field(index=True, unique=True)
    description: Optional[str] = None
    min_players: int = Field(gt=0)
    max_players: int = Field(gt=0)


### Represents a game in the db
class Game(GameBase, table=True):
    __table_name__ = "game"
    id: UUID | None = Field(default_factory=uuid4, primary_key=True) # Will be fed by the db

### Represents data needed to create a new game
class GameCreate(GameBase):
    pass


