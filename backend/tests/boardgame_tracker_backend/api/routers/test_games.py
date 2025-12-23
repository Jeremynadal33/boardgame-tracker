from boardgame_tracker_backend.api.routers.games import router as games_router
from boardgame_tracker_backend.core.config import settings

from fastapi.testclient import TestClient

#### Testing api/v1/games endpoints ####
games_endpoint = f"{settings.API_V1_STR}/games/"

def test_create_game(client: TestClient) -> None:
    game_data = {
        "name": "Catn",
        "min_players": 3,
        "max_players": 4,
        "description": "A popular board game"
    }
    response = client.post(games_endpoint, json=game_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Catn"
    assert data["min_players"] == 3
    assert data["max_players"] == 4
    assert data["description"] == "A popular board game"

def test_list_games(client: TestClient) -> None:
    response = client.get(games_endpoint)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
