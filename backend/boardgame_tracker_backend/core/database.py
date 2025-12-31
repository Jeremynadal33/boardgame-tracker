from sqlmodel import Session, create_engine, select
from boardgame_tracker_backend.core.config import settings

# Engine is the low-level interface to the database
# We will use it to create sessions that allows us
# to interact with the database with more control
# using transactions and allowing us to map models to tables (ORM)

if settings.DATABASE_TYPE == "sqlite":
    engine = create_engine(str(settings.DATABASE_URL))
else:
    raise ValueError(f"Unsupported database type: {settings.DATABASE_TYPE}")


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    from sqlmodel import SQLModel

    # This works because only if models were imported !
    # It does not create tables if models are not imported
    # It does not allow altering existing tables either
    # Does not overrite existing data
    SQLModel.metadata.create_all(engine)
    dummy_data(session)


if __name__ == "__main__":
    # Simple test to check if the database connection works
    with Session(engine) as session:
        result = session.exec(select(1)).first()
        init_db(session)


def dummy_data(session: Session) -> None:
    from boardgame_tracker_backend.models.player import Player
    from boardgame_tracker_backend.models.game import Game

    # Add a dummy player

    dummy_player = Player(pseudo="toto", email="toto@toto.com", hashed_password="$2b$12$.cDdQZfBLAKRouyn66k/ieCaVVcB/23bQbWw42vEOMFJkB0oKN3WC")
    
    if not session.exec(select(Player).where(Player.email == dummy_player.email)).first():
        session.add(dummy_player)
        session.commit()
        session.refresh(dummy_player)
        print("Added dummy player:", dummy_player)