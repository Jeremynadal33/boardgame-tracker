from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field, Column, TIMESTAMP, text
from pydantic import EmailStr

from datetime import datetime

class PlayerBase(SQLModel):
    pseudo: str = Field(index=True, unique=True)
    email: EmailStr = Field(unique=True)
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
    created_datetime: datetime | None = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
    ))
    updated_datetime: datetime | None = Field(sa_column=Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP"),
        server_onupdate=text("CURRENT_TIMESTAMP"),
    ))
    # TODO: add FKs once relationships are defined

### Represents data needed to create a new player
class PlayerCreate(PlayerBase):
    password: str