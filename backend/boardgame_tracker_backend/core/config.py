import secrets

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_TYPE: str = "sqlite"  # Default to sqlite if not specified
    PROJECT_NAME: str

    model_config = SettingsConfigDict(env_file=".env")

    API_V1_STR: str = "/api/v1"

    # Generate a random secret key if not provided, for development purposes
    SECRET_KEY: str = secrets.token_urlsafe(32)

    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # print("Loading settings from .env file")
    # print(f"model_config: {model_config}")


settings = Settings()
