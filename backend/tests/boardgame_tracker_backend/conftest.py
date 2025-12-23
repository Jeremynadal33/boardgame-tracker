from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete

from boardgame_tracker_backend.core.config import settings
from boardgame_tracker_backend.core.database import engine, init_db
from boardgame_tracker_backend.main import app
from boardgame_tracker_backend.models.game import Game


# scope session means that the fixture is created once per test session
# It yields a session to be used in tests and cleans up after all tests are done
@pytest.fixture(scope="function", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        init_db(session)
        yield session
        statement = delete(Game)
        session.exec(statement)
        session.commit()

# scope module means that the fixture is created once per test module
# It yields a TestClient to be used in tests so we can make requests to the FastAPI app
@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    with TestClient(app) as c:
        yield c
