import pytest
from uuid import uuid4
from datetime import timedelta
from fastapi import HTTPException
from sqlmodel import Session

from boardgame_tracker_backend.api.dependencies import get_current_player
from boardgame_tracker_backend.models.player import Player, TokenPayload
from boardgame_tracker_backend.core import security

class TestGetCurrentPlayer:
    
    def test_get_current_player_success(self, db: Session) -> None:
        """Test successful retrieval of current player with valid token"""
        # Create a test player in the database
        player = Player(
            pseudo="testplayer",
            email="test@example.com",
            hashed_password="hashed_password",
            is_active=True
        )
        db.add(player)
        db.commit()
        db.refresh(player)
        
        # Create a valid token for this player
        token = security.create_access_token(
            subject=str(player.id), 
            expires_delta=timedelta(hours=1)
        )
        
        # Test the function
        result = get_current_player(db, token)
        
        assert result.id == player.id
        assert result.pseudo == "testplayer"
        assert result.is_active is True

    def test_get_current_player_expired_token(self, db: Session) -> None:
        """Test that expired token raises 401 Unauthorized"""
        # Create an expired token (negative time delta)
        expired_token = security.create_access_token(
            subject=str(uuid4()), 
            expires_delta=timedelta(seconds=-1)
        )
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_player(db, expired_token)
        
        assert exc_info.value.status_code == 401
        assert exc_info.value.detail == "Token has expired"

    def test_get_current_player_invalid_token(self, db: Session) -> None:
        """Test that invalid token raises 403 Forbidden"""
        invalid_token = "invalid.jwt.token"
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_player(db, invalid_token)
        
        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Could not validate credentials"

    def test_get_current_player_nonexistent_player(self, db: Session) -> None:
        """Test that valid token for nonexistent player raises 404 Not Found"""
        # Create a valid token for a player that doesn't exist in the database
        nonexistent_player_id = str(uuid4())
        token = security.create_access_token(
            subject=nonexistent_player_id, 
            expires_delta=timedelta(hours=1)
        )
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_player(db, token)
        
        assert exc_info.value.status_code == 404
        assert exc_info.value.detail == "Player not found"

    def test_get_current_player_inactive_player(self, db: Session) -> None:
        """Test that token for inactive player raises 403 Forbidden"""
        # Create an inactive player in the database
        inactive_player = Player(
            pseudo="inactiveplayer",
            email="inactive@example.com",
            hashed_password="hashed_password",
            is_active=False
        )
        db.add(inactive_player)
        db.commit()
        db.refresh(inactive_player)
        
        # Create a valid token for this inactive player
        token = security.create_access_token(
            subject=str(inactive_player.id), 
            expires_delta=timedelta(hours=1)
        )
        
        with pytest.raises(HTTPException) as exc_info:
            get_current_player(db, token)
        
        assert exc_info.value.status_code == 403
        assert exc_info.value.detail == "Inactive player"