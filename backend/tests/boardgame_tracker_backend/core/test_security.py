from datetime import datetime, timedelta, timezone
import jwt
import pytest

from boardgame_tracker_backend.core.security import (
    create_access_token,
    decode_access_token,
    verify_password,
    get_password_hash,
    ALGORITHM
)
from boardgame_tracker_backend.core.config import settings


class TestCreateAccessToken:
    def test_create_access_token_success(self):
        """Test that create_access_token returns a string."""
        subject = "test_user"
        expires_delta = timedelta(minutes=30)
        
        token = create_access_token(subject, expires_delta)
        
        assert isinstance(token, str)
        assert len(token) > 0

    def test_create_access_token_valid_jwt(self):
        """Test that the created token is a valid JWT."""
        subject = "test_user"
        expires_delta = timedelta(minutes=30)
        expected_exp = datetime.now(timezone.utc) + expires_delta

        token = create_access_token(subject, expires_delta)
        
        # Should be able to decode without raising an exception
        decoded = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])

        # Allow 1 second tolerance for timing differences
        exp_time = datetime.fromtimestamp(decoded["exp"], tz=timezone.utc)
        assert abs((exp_time - expected_exp).total_seconds()) < 1

        assert decoded["sub"] == subject
        assert "exp" in decoded

    def test_create_access_token_different_subjects(self):
        """Test that different subjects create different tokens."""
        expires_delta = timedelta(minutes=30)
        
        token1 = create_access_token("user1", expires_delta)
        token2 = create_access_token("user2", expires_delta)
        
        assert token1 != token2
        
        decoded1 = jwt.decode(token1, settings.SECRET_KEY, algorithms=[ALGORITHM])
        decoded2 = jwt.decode(token2, settings.SECRET_KEY, algorithms=[ALGORITHM])
        
        assert decoded1["sub"] == "user1"
        assert decoded2["sub"] == "user2"


class TestDecodeAccessToken:
    def test_decode_access_token_valid_token(self):
        """Test decoding a valid token."""
        subject = "test_user"
        expires_delta = timedelta(minutes=30)
        
        token = create_access_token(subject, expires_delta)
        decoded = decode_access_token(token)
        
        assert decoded["sub"] == subject
        assert "exp" in decoded

    def test_decode_access_token_invalid_token(self):
        """Test that decoding an invalid token raises an exception."""
        with pytest.raises(jwt.DecodeError):
            decode_access_token("invalid.token.here")

    def test_decode_access_token_expired_token(self):
        """Test that decoding an expired token raises an exception."""
        subject = "test_user"
        expires_delta = timedelta(seconds=-1)  # Already expired
        
        token = create_access_token(subject, expires_delta)
        
        with pytest.raises(jwt.ExpiredSignatureError):
            decode_access_token(token)


class TestPasswordFunctions:
    def test_password_hash_and_verify(self):
        """Test password hashing and verification."""
        password = "test_password_123"
        hashed = get_password_hash(password)
        
        assert hashed != password  # Should be hashed
        assert verify_password(password, hashed) is True
        assert verify_password("wrong_password", hashed) is False

    def test_different_passwords_different_hashes(self):
        """Test that different passwords create different hashes."""
        password1 = "password1"
        password2 = "password2"
        
        hash1 = get_password_hash(password1)
        hash2 = get_password_hash(password2)
        
        assert hash1 != hash2
    
    def test_same_password_different_hashes(self):
        """Test that the same password creates different hashes due to salting."""
        password = "same_password"
        
        hash1 = get_password_hash(password)
        hash2 = get_password_hash(password)
        
        assert hash1 != hash2
