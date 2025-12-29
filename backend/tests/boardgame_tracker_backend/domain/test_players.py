from boardgame_tracker_backend.domain.players import (
    register_player,
    PlayerAlreadyExistsError,
)
from boardgame_tracker_backend.models.player import PlayerCreate

from sqlmodel import Session
from pytest import raises

player_in = PlayerCreate(
    pseudo="toto", email="toto@gmail.com", password="securepassword123"
)


def test_register_player_success(db: Session) -> None:
    player = register_player(session=db, player_in=player_in)

    assert player.id is not None
    assert player.pseudo == "toto"
    assert player.email == "toto@gmail.com"


def test_register_player_pseudo_already_exists(db: Session) -> None:
    # First creation should succeed
    register_player(session=db, player_in=player_in)

    # Second creation with the same email should raise an error
    updated_player_in = player_in.model_copy()
    updated_player_in.email = "other@gmail.com"
    with raises(PlayerAlreadyExistsError) as exc_info:
        register_player(session=db, player_in=updated_player_in)

    assert exc_info.value.type == "pseudo"
    assert exc_info.value.input == "toto"


def test_register_player_email_already_exists(db: Session) -> None:
    # First creation should succeed
    register_player(session=db, player_in=player_in)

    # Second creation with the same email should raise an error
    updated_player_in = player_in.model_copy()
    updated_player_in.pseudo = "otherpseudo"
    with raises(PlayerAlreadyExistsError) as exc_info:
        register_player(session=db, player_in=updated_player_in)

    assert exc_info.value.type == "email"
    assert exc_info.value.input == "toto@gmail.com"
