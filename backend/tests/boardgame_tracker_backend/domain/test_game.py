from boardgame_tracker_backend.domain.games import create_game, list_games, GameAlreadyExistsError, GameCreationError
from boardgame_tracker_backend.models.game import Game, GameCreate

from sqlmodel import Session

from pytest import raises

catan_game_in = GameCreate(
    name="Catan",
    min_players=3,
    max_players=4,
    description="A popular board game"
)

def test_create_game_success(db: Session) -> None:
    
    game = create_game(session=db, game_in=catan_game_in)

    assert game.id is not None
    assert game.name == "Catan"
    assert game.min_players == 3
    assert game.max_players == 4
    assert game.description == "A popular board game"

def test_create_game_already_exists(db: Session) -> None:    
    # First creation should succeed
    create_game(session=db, game_in=catan_game_in)

    # Second creation with the same name should raise an error
    with raises(GameAlreadyExistsError):
        create_game(session=db, game_in=catan_game_in)


## Not sure how to simulate other Errors in this context


def test_list_games(db: Session) -> None:
    # db is always cleaned up between tests, so we can add games here
    game2 = GameCreate(
        name="Pandemic",
        min_players=2,
        max_players=4,
        description="A cooperative board game"
    )

    create_game(session=db, game_in=catan_game_in)
    create_game(session=db, game_in=game2)

    games = list_games(session=db)
    assert len(games) == 2
    print(games[0])
    game_names = {game.name for game in games}
    assert "Catan" in game_names
    assert "Pandemic" in game_names