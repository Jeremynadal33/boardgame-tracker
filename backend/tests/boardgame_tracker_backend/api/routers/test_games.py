from boardgame_tracker_backend.core.config import settings

from fastapi.testclient import TestClient

#### Testing api/v1/games endpoints ####
games_endpoint = f"{settings.API_V1_STR}/games/"

def test_create_game_success(client: TestClient) -> None:
    game_data = {
        "name": "Catan",
        "min_players": 3,
        "max_players": 4,
        "description": "A popular board game"
    }
    response = client.post(games_endpoint, json=game_data)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Catan"
    assert data["min_players"] == 3
    assert data["max_players"] == 4
    assert data["description"] == "A popular board game"

def test_create_game_already_exists(client: TestClient) -> None:
    game_data = {
        "name": "Catan",
        "min_players": 3,
        "max_players": 4,
        "description": "A popular board game"
    }
    response = client.post(games_endpoint, json=game_data)
    assert response.status_code == 200

    response = client.post(games_endpoint, json=game_data)

    data = response.json()
    assert response.status_code == 409 # Conflict
    assert data["detail"] == "A game with the name 'Catan' already exists"

def test_create_game_missing_name(client: TestClient) -> None:
    game_data = {
        "min_players": 2,
        "max_players": 4,
        "description": "A game without a name"
    }
    response = client.post(games_endpoint, json=game_data)
    assert response.status_code == 422  # Unprocessable Entity returned by FastAPI for validation errors

def test_list_games(client: TestClient) -> None:
    response = client.get(games_endpoint)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
