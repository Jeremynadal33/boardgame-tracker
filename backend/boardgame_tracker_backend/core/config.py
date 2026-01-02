from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///boardgame_tracker.db"
    DATABASE_TYPE: str = "sqlite"  # Default to sqlite if not specified
    PROJECT_NAME: str = "Boardgame Tracker"
    ENV: str = "dev"

    model_config = SettingsConfigDict(env_file=".env")

    API_V1_STR: str = "/api/v1"
    LOGIN_ENDPOINT: str = f"{API_V1_STR}/players/login/access-token"

    # Generate a random secret key if not provided, for development purposes
    SECRET_KEY: str = "lasuperclefsecretouais"  # secrets.token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # print("Loading settings from .env file")
    # print(f"model_config: {model_config}")


settings = Settings()
