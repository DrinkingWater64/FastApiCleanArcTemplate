import os
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App Config
    PROJECT_NAME: str = "Clean Architecture FastAPI"
    API_V1_STR: str = "/api/v1"

    # Database Config
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/clean_arch_db"

    # This tells Pydantic to read from a file named ".env"
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore"  # Ignore extra env variables that might be in the system
    )

settings = Settings()