from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from pydantic import EmailStr
from typing import Sequence

from datetime import datetime, timezone


class PlayerBase(SQLModel):
    pseudo: str = Field(index=True, unique=True, max_length=30)
    email: EmailStr = Field(unique=True, max_length=100)
    is_superuser: bool = False
    # Optional for stats & maybe later teammate findings
    city: str | None = None
    country: str | None = None
    # Not sure how to use the following but feel like it could be useful
    is_active: bool = True


### Represents a player in the db
class Player(PlayerBase, table=True):
    __table_name__ = "player"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )
    updated_at: datetime | None = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        sa_column_kwargs={"onupdate": lambda: datetime.now(timezone.utc)},
    )
    # TODO: add FKs once relationships are defined


### Represents data needed to create a new player
class PlayerCreate(PlayerBase):
    password: str = Field(min_length=8, max_length=72)


### Represents data needed to update a player, everything optional
### Cannot update email or id so we can't inherite from PlayerBase
class PlayerUpdate(SQLModel):
    pseudo: str | None = Field(default=None, max_length=30)
    password: str | None = Field(default=None, min_length=8, max_length=72)
    city: str | None = None
    country: str | None = None


### Represents a player that can be publicly shared
class PlayerPublic(PlayerBase):
    id: UUID


### Represents a list of players that can be publicly shared
class PlayersPublic(SQLModel):
    players: Sequence[PlayerPublic]
    count: int


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: str | None = None


class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
