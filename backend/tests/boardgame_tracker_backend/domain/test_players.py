from boardgame_tracker_backend.domain.players import (
    register_player,
    update_player,
    PlayerAlreadyExistsError,
    get_player_by_email,
    list_players,
    authenticate,
    create_access_token,
    PlayerNotFoundError,
    InvalidCredentialsError,
    InactivePlayerError,
)

from boardgame_tracker_backend.core.security import verify_password

from boardgame_tracker_backend.models.player import (
    PlayerCreate,
    PlayersPublic,
    Token,
    PlayerUpdate,
)

from sqlmodel import Session
from pytest import raises
import pytest

player_in = PlayerCreate(
    pseudo="toto", email="toto@gmail.com", password="securepassword123"
)


class TestRegisterPlayer:
    def test_register_player_success(self, db: Session) -> None:
        player = register_player(session=db, player_in=player_in)

        assert player.id is not None
        assert player.pseudo == "toto"
        assert player.email == "toto@gmail.com"

    def test_register_player_pseudo_already_exists(self, db: Session) -> None:
        # First creation should succeed
        register_player(session=db, player_in=player_in)

        # Second creation with the same email should raise an error
        player_update_data = player_in.model_copy()
        player_update_data.email = "other@gmail.com"
        with raises(PlayerAlreadyExistsError) as exc_info:
            register_player(session=db, player_in=player_update_data)

        assert exc_info.value.type == "pseudo"
        assert exc_info.value.input == "toto"

    def test_register_player_email_already_exists(self, db: Session) -> None:
        # First creation should succeed
        register_player(session=db, player_in=player_in)

        # Second creation with the same email should raise an error
        player_update_data = player_in.model_copy()
        player_update_data.pseudo = "otherpseudo"
        with raises(PlayerAlreadyExistsError) as exc_info:
            register_player(session=db, player_in=player_update_data)

        assert exc_info.value.type == "email"
        assert exc_info.value.input == "toto@gmail.com"


class TestUpdatePlayer:
    def test_update_player_update_password_success(self, db: Session) -> None:
        # Create a player first
        created_player = register_player(session=db, player_in=player_in)
        new_password = "newsecurepassword456"
        player_update = PlayerUpdate(password=new_password)

        updated_player = update_player(
            session=db, db_player=created_player, player_in=player_update
        )

        assert updated_player.id == created_player.id
        assert updated_player.pseudo == created_player.pseudo
        assert verify_password(new_password, updated_player.hashed_password)

    def test_update_player_update_pseudo_success(self, db: Session) -> None:
        # Create a player first
        created_player = register_player(session=db, player_in=player_in)
        new_pseudo = "newtoto"
        player_update = PlayerUpdate(pseudo=new_pseudo)

        updated_player = update_player(
            session=db, db_player=created_player, player_in=player_update
        )

        assert updated_player.id == created_player.id
        assert updated_player.pseudo == new_pseudo
        assert updated_player.email == created_player.email

    def test_update_player_update_city_country_success(self, db: Session) -> None:
        # Create a player first
        created_player = register_player(session=db, player_in=player_in)
        player_update_data = PlayerUpdate(country="New Country", city="New City")

        updated_player = update_player(
            session=db, db_player=created_player, player_in=player_update_data
        )

        assert updated_player.id == created_player.id
        assert updated_player.city == "New City"
        assert updated_player.country == "New Country"

    def test_update_player_pseudo_already_exists(self, db: Session) -> None:
        # Create two players first
        register_player(session=db, player_in=player_in)
        another_player_in = PlayerCreate(
            pseudo="alice", email="alice@gmail.com", password="anothersecurepassword"
        )
        another_created_player = register_player(
            session=db, player_in=another_player_in
        )

        # Attempt to update second player's pseudo to first player's pseudo
        player_update = PlayerUpdate(pseudo="toto")

        with raises(PlayerAlreadyExistsError):
            update_player(
                session=db,
                db_player=another_created_player,
                player_in=player_update,
            )


class TestListPlayers:
    def test_list_players(self, db: Session) -> None:
        # Create multiple players
        created_player = register_player(session=db, player_in=player_in)
        another_player_in = PlayerCreate(
            pseudo="alice", email="alice@gmail.com", password="anothersecurepassword"
        )
        another_created_player = register_player(
            session=db, player_in=another_player_in
        )

        players_public = list_players(session=db)

        assert len(players_public.players) == 2
        assert isinstance(players_public, type(PlayersPublic(count=0, players=[])))
        assert players_public.count == 2
        assert created_player.id in [p.id for p in players_public.players]
        assert another_created_player.id in [p.id for p in players_public.players]


class TestGetPlayerByEmail:
    def test_get_player_by_email_success(self, db: Session) -> None:
        created_player = register_player(session=db, player_in=player_in)

        player = get_player_by_email(session=db, email="toto@gmail.com")

        assert player is not None
        assert isinstance(player, type(created_player))
        assert created_player.id == player.id
        assert player.pseudo == "toto"
        assert player.email == "toto@gmail.com"

    def test_get_player_by_email_not_found(self, db: Session) -> None:
        player = get_player_by_email(session=db, email="nonexistent@gmail.com")
        assert player is None


class TestAuthenticate:
    def test_authenticate_success(self, db: Session) -> None:
        """Test successful authentication with correct credentials"""
        # Create a player first
        created_player = register_player(session=db, player_in=player_in)

        # Authenticate with correct credentials
        authenticated_player = authenticate(
            session=db, email="toto@gmail.com", password="securepassword123"
        )

        assert authenticated_player is not None
        assert authenticated_player.id == created_player.id
        assert authenticated_player.email == "toto@gmail.com"
        assert authenticated_player.pseudo == "toto"

    def test_authenticate_player_not_found(self, db: Session) -> None:
        """Test authentication fails when player doesn't exist"""
        with raises(PlayerNotFoundError):
            authenticate(
                session=db, email="nonexistent@gmail.com", password="anypassword"
            )

    @pytest.mark.parametrize("password", ["wrongpassword", "", " securepassword123 "])
    def test_authenticate_different_passwords(self, password, db: Session) -> None:
        """Test authentication fails with different passwords"""
        # Create a player first
        register_player(session=db, player_in=player_in)

        with raises(InvalidCredentialsError):
            authenticate(session=db, email="toto@gmail.com", password=password)

    def test_authenticate_whitespace_in_credentials(self, db: Session) -> None:
        """Test authentication with whitespace in credentials"""
        # Create a player first
        register_player(session=db, player_in=player_in)

        # Email with whitespace should fail (exact match required)
        with raises(PlayerNotFoundError):
            authenticate(
                session=db, email=" toto@gmail.com ", password="securepassword123"
            )


class TestCreateAccessToken:
    def test_create_access_token_success(self, db: Session) -> None:
        """Test successful token creation for valid, active player"""
        # Create a player first
        register_player(session=db, player_in=player_in)

        # Create access token with correct credentials
        token = create_access_token(
            session=db, email="toto@gmail.com", password="securepassword123"
        )

        assert token is not None
        assert isinstance(token, Token)
        assert token.access_token is not None
        assert len(token.access_token) > 0

    def test_create_access_token_inactive_player(self, db: Session) -> None:
        """Test token creation fails for inactive player"""
        # Create a player first
        created_player = register_player(session=db, player_in=player_in)

        # Set player as inactive
        created_player.is_active = False
        db.add(created_player)
        db.commit()

        # Try to create token for inactive player
        with raises(InactivePlayerError):
            create_access_token(
                session=db, email="toto@gmail.com", password="securepassword123"
            )

    @pytest.mark.parametrize(
        "email,password,expected_exception",
        [
            ("nonexistent@gmail.com", "validpassword", PlayerNotFoundError),
            ("toto@gmail.com", "wrongpassword", InvalidCredentialsError),
        ],
    )
    def test_create_access_token_authentication_failures(
        self, email, password, expected_exception, db: Session
    ) -> None:
        """Test token creation fails with invalid credentials"""
        # Create a player for the second test case
        if email == "toto@gmail.com":
            register_player(session=db, player_in=player_in)

        # Verify appropriate exception is raised
        with raises(expected_exception):
            create_access_token(session=db, email=email, password=password)
