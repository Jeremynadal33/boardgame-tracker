from boardgame_tracker_backend.core.config import settings

from fastapi.testclient import TestClient

#### Testing api/v1/players endpoints ####
players_base_endpoint = f"{settings.API_V1_STR}/players/"

def test_create_player_success(client: TestClient) -> None:
    player_data = {
        "pseudo": "toto",
        "email": "toto@gmail.com",
        "password": "securepassword123"
    }
    response = client.post(players_base_endpoint + "signup", json=player_data)
    assert response.status_code == 200
    data = response.json()
    assert data["pseudo"] == "toto"
    assert data["email"] == "toto@gmail.com"
    assert "hashed_password" not in data  # Ensure password is not returned