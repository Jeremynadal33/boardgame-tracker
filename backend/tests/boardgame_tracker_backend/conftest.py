from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, delete, create_engine, SQLModel
from sqlalchemy.pool import StaticPool

from boardgame_tracker_backend.main import app
from boardgame_tracker_backend.models.game import Game
from boardgame_tracker_backend.api.dependencies import get_db

IN_MEMORY_TESTING_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    IN_MEMORY_TESTING_DATABASE_URL,
    connect_args={
        "check_same_thread": False,
    },
    poolclass=StaticPool,
)

# scope "function" means that the fixture is created once per test function
# It yields a session to be used in tests and cleans up after each test function is done
@pytest.fixture(scope="function", autouse=True)
def db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        # init_db(session) # Should we use the same int_db as production ?

        SQLModel.metadata.drop_all(engine) # Surely not needed with in-memory DB but just in case
        SQLModel.metadata.create_all(engine)
        yield session
        # Cleanup after test
        SQLModel.metadata.drop_all(engine)


def get_test_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        SQLModel.metadata.create_all(engine)
        yield session

# scope module means that the fixture is created once per test module
# It yields a TestClient to be used in tests so we can make requests to the FastAPI app
@pytest.fixture(scope="module")
def client() -> Generator[TestClient, None, None]:
    # Override the database dependency to use the test database
    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as c:
        yield c
    # Clean up the override after tests
    app.dependency_overrides.clear()
