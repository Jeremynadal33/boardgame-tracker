import pytest
from pydantic import ValidationError

from boardgame_tracker_backend.core.config import DEFAULT_SECRET_KEY, Settings


def build_settings(**overrides: object) -> Settings:
    return Settings(_env_file=None, **overrides)  # type: ignore[call-arg]


def test_dev_allows_default_secret_key_and_insecure_cookie() -> None:
    config = build_settings(ENV="dev")

    assert config.SECRET_KEY == DEFAULT_SECRET_KEY
    assert config.COOKIE_SECURE is False


def test_prod_refuses_default_secret_key() -> None:
    with pytest.raises(ValidationError, match="SECRET_KEY"):
        build_settings(ENV="prod")


def test_prod_defaults_to_secure_cookie() -> None:
    config = build_settings(ENV="prod", SECRET_KEY="a-real-secret")

    assert config.COOKIE_SECURE is True


def test_cookie_secure_can_be_overridden() -> None:
    config = build_settings(ENV="prod", SECRET_KEY="a-real-secret", COOKIE_SECURE=False)

    assert config.COOKIE_SECURE is False
