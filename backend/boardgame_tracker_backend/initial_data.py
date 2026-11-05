import logging

from sqlmodel import Session

# Import all models to ensure they are registered with SQLModel
import boardgame_tracker_backend.models  # noqa: F401
from boardgame_tracker_backend.core.database import engine, init_db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def init() -> None:
    with Session(engine) as session:
        init_db(session)


def main() -> None:
    logger.info("Creating initial data")
    init()
    logger.info("Initial data created")


if __name__ == "__main__":
    main()
