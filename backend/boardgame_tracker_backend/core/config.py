from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_SECRET_KEY = "lasuperclefsecretouais"


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///boardgame_tracker.db"
    DATABASE_TYPE: str = "sqlite"  # Default to sqlite if not specified
    PROJECT_NAME: str = "Boardgame Tracker"
    ENV: str = "dev"
    # Directory of the built frontend; when unset, only the API is served
    STATIC_DIR: str | None = None

    model_config = SettingsConfigDict(env_file=".env")

    API_V1_STR: str = "/api/v1"
    LOGIN_ENDPOINT: str = f"{API_V1_STR}/players/login/access-token"

    # Generate a random secret key if not provided, for development purposes
    SECRET_KEY: str = DEFAULT_SECRET_KEY  # secrets.token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    ACCESS_TOKEN_COOKIE_NAME: str = "access_token"
    # Secure cookies are only sent over https: when unset, they are disabled in dev only.
    COOKIE_SECURE: bool | None = None
    # Extra origins (e.g. https://app.example.com) allowed to call state-changing
    # endpoints, in addition to the host the request was sent to.
    ALLOWED_ORIGINS: list[str] = []

    @model_validator(mode="after")
    def _apply_environment_defaults(self) -> "Settings":
        if self.ENV != "dev" and self.SECRET_KEY == DEFAULT_SECRET_KEY:
            raise ValueError("SECRET_KEY must be set when ENV is not 'dev'")
        if self.COOKIE_SECURE is None:
            self.COOKIE_SECURE = self.ENV != "dev"
        return self

    # print("Loading settings from .env file")
    # print(f"model_config: {model_config}")


settings = Settings()
