from uuid import UUID, uuid4
from sqlmodel import SQLModel, Field
from pydantic import EmailStr

### Represents a player in the db
class Player(SQLModel, table=True):
    __table_name__ = "player"
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    name: str = Field(index=True)
    email: EmailStr = Field(unique=True)
    hashed_password: str
