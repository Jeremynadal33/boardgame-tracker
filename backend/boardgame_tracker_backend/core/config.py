from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    DATABASE_TYPE: str = "sqlite"  # Default to sqlite if not specified
    PROJECT_NAME: str

    model_config = SettingsConfigDict(env_file=".env")

    API_V1_STR: str = "/api/v1"

    # print("Loading settings from .env file")
    # print(f"model_config: {model_config}")

settings = Settings()