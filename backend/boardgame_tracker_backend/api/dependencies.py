from sqlmodel import Session
from fastapi import Depends

from collections.abc import Generator

from typing import Annotated

from boardgame_tracker_backend.core.database import engine


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]