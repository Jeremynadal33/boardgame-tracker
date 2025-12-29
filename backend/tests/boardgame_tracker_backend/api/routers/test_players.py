from boardgame_tracker_backend.core.config import settings
from boardgame_tracker_backend.domain import players
from boardgame_tracker_backend.models.player import Token

from fastapi.testclient import TestClient
import pytest
from unittest.mock import patch, MagicMock

#### Testing api/v1/players endpoints ####
players_base_endpoint = f"{settings.API_V1_STR}/players/"

class TestRegisterPlayer:
    """Tests for the /players/signup endpoint"""
    register_url = players_base_endpoint + "signup"
    
    def test_create_player_success(self, client: TestClient) -> None:
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


class TestLoginAccessToken:
    """Tests for the /players/login/access-token endpoint"""
    login_url = players_base_endpoint + "login/access-token"
    login_data = {
        "username": "test@example.com",
        "password": "testpassword"
    }
        
    @patch("boardgame_tracker_backend.domain.players.create_access_token")
    def test_login_access_token_success(self, mock_create_token, client: TestClient) -> None:
        """Test successful login returns access token"""
        
        mock_token = Token(access_token="fake-jwt-token", token_type="bearer")
        mock_create_token.return_value = mock_token
        
        response = client.post(
            self.login_url,
            data=self.login_data,  # OAuth2PasswordRequestForm expects form data, not JSON
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["access_token"] == "fake-jwt-token"
        assert data["token_type"] == "bearer"


    @patch("boardgame_tracker_backend.domain.players.create_access_token")
    def test_login_access_token_player_not_found(self, mock_create_token, client: TestClient) -> None:
        """Test login with non-existent user returns 400 error"""
        login_data = self.login_data.copy()
        login_data["username"] = "nonexistent@example.com"
        
        mock_create_token.side_effect = players.PlayerNotFoundError()
        
        response = client.post(
            self.login_url,
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert "Player with email nonexistent@example.com not found" in data["detail"]


    @patch("boardgame_tracker_backend.domain.players.create_access_token")
    def test_login_access_token_invalid_credentials(self, mock_create_token, client: TestClient) -> None:
        """Test login with wrong password returns 400 error"""
        login_data = self.login_data.copy()
        login_data["password"] = "wrongpassword"
        
        mock_create_token.side_effect = players.InvalidCredentialsError()
        
        response = client.post(
            self.login_url,
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 400
        data = response.json()
        assert data["detail"] == "Incorrect email or password"


    @patch("boardgame_tracker_backend.domain.players.create_access_token")
    def test_login_access_token_token_creation_error(self, mock_create_token, client: TestClient) -> None:
        """Test login when token creation fails returns 500 error"""
        mock_create_token.side_effect = players.TokenCreationError("Token service unavailable")
        
        response = client.post(
            self.login_url,
            data=self.login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "Token service unavailable"


    @patch("boardgame_tracker_backend.domain.players.create_access_token")
    def test_login_access_token_unexpected_error(self, mock_create_token, client: TestClient) -> None:
        """Test login when unexpected error occurs returns 500 error"""        
        mock_create_token.side_effect = RuntimeError("Database connection lost")
        
        response = client.post(
            self.login_url,
            data=self.login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "An unexpected error occurred"


    @pytest.mark.parametrize("missing_field", ["username", "password"])
    def test_login_access_token_missing_required_fields(self, client: TestClient, missing_field: str) -> None:
        """Test login with missing required fields returns validation error"""
        login_data = self.login_data.copy()
        del login_data[missing_field]
        
        response = client.post(
            self.login_url,
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        assert response.status_code == 422  # Unprocessable Entity for validation errors
        data = response.json()
        assert "detail" in data


    def test_login_access_token_empty_credentials(self, client: TestClient) -> None:
        """Test login with empty username/password"""
        login_data = {
            "username": "",
            "password": ""
        }
        
        response = client.post(
            self.login_url,
            data=login_data,
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )
        
        # Unprocessable Entity for validation errors
        assert response.status_code == 422