from fastapi.testclient import TestClient
from sqlmodel import Session

from boardgame_tracker_backend.core.config import settings
from boardgame_tracker_backend.models.player import PlayerCreate, PlayerUpdate
from boardgame_tracker_backend.domain import players
from boardgame_tracker_backend.domain.players import register_player

from tests.boardgame_tracker_backend.utils.utils import (
    random_lower_string,
    random_email,
)


def create_random_player(db: Session) -> players.Player:
    """Helper function to create a test player"""
    player_in = PlayerCreate(
        pseudo=random_lower_string(),
        email=random_email(),
        password=random_lower_string(),
    )
    return register_player(session=db, player_in=player_in)


def player_authentication_headers(
    *, client: TestClient, email: str, password: str
) -> dict[str, str]:
    data = {"username": email, "password": password}

    r = client.post(settings.LOGIN_ENDPOINT, data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def authentication_token_from_email(
    *, client: TestClient, email: str, db: Session
) -> dict[str, str]:
    """
    Return a valid token for the player with given email.

    If the player doesn't exist it is created first.
    """
    password = random_lower_string()
    pseudo = random_lower_string()
    player = players.get_player_by_email(session=db, email=email)
    if not player:
        player_in = PlayerCreate(pseudo=pseudo, email=email, password=password)
        players.register_player(session=db, player_in=player_in)
    else:
        player_in_update = PlayerUpdate(password=password)
        if not player.id:
            raise players.PlayerUpdateError("Player id not set")
        players.update_player(session=db, db_player=player, player_in=player_in_update)

    return player_authentication_headers(client=client, email=email, password=password)
