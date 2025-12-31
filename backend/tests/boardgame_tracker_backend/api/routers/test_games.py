from boardgame_tracker_backend.core.config import settings

from fastapi.testclient import TestClient

#### Testing api/v1/games endpoints ####
games_endpoint = f"{settings.API_V1_STR}/games/"


class TestCreateGame:
    """Must be logged in to create a game"""

    def test_create_game_success(
        self, client: TestClient, normal_player_token_headers: dict[str, str]
    ) -> None:
        game_data = {
            "name": "Catan",
            "min_players": 3,
            "max_players": 4,
            "description": "A popular board game",
        }
        response = client.post(
            games_endpoint, json=game_data, headers=normal_player_token_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Catan"
        assert data["min_players"] == 3
        assert data["max_players"] == 4
        assert data["description"] == "A popular board game"

    def test_create_game_already_exists(
        self, client: TestClient, normal_player_token_headers: dict[str, str]
    ) -> None:
        game_data = {
            "name": "Catan",
            "min_players": 3,
            "max_players": 4,
            "description": "A popular board game",
        }
        response = client.post(
            games_endpoint, json=game_data, headers=normal_player_token_headers
        )
        assert response.status_code == 201

        response = client.post(
            games_endpoint, json=game_data, headers=normal_player_token_headers
        )

        data = response.json()
        assert response.status_code == 409  # Conflict
        assert data["detail"] == "A game with the name 'Catan' already exists"

    def test_create_game_missing_name(
        self, client: TestClient, normal_player_token_headers: dict[str, str]
    ) -> None:
        game_data = {
            "min_players": 2,
            "max_players": 4,
            "description": "A game without a name",
        }
        response = client.post(
            games_endpoint, json=game_data, headers=normal_player_token_headers
        )
        assert (
            response.status_code == 422
        )  # Unprocessable Entity returned by FastAPI for validation errors


class TestListGames:
    def test_list_games_no_games(self, client: TestClient) -> None:
        response = client.get(games_endpoint)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    def test_list_games_with_games(
        self, client: TestClient, normal_player_token_headers: dict[str, str]
    ) -> None:
        game_data_1 = {
            "name": "Catan",
            "min_players": 3,
            "max_players": 4,
            "description": "A popular board game",
        }
        game_data_2 = {
            "name": "Pandemic",
            "min_players": 2,
            "max_players": 4,
            "description": "A cooperative board game",
        }
        client.post(
            games_endpoint, json=game_data_1, headers=normal_player_token_headers
        )
        client.post(
            games_endpoint, json=game_data_2, headers=normal_player_token_headers
        )

        response = client.get(games_endpoint)
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 2
        game_names = {game["name"] for game in data}
        assert "Catan" in game_names
        assert "Pandemic" in game_names
