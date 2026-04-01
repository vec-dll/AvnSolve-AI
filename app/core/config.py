from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str
    gemini_api_key: str
    groq_api_key: str
    database_url: str = "sqlite+aiosqlite:///./app.db"
    app_env: str = "development"
    log_level: str = "INFO"
    max_context_messages: int = 12
    max_image_size_mb: int = 10
    default_ui_language: str = "ru"

    @field_validator("database_url", mode="before")
    @classmethod
    def normalize_database_url(cls, value: str) -> str:
        if value.startswith("postgres://"):
            return "postgresql+asyncpg://" + value[len("postgres://") :]
        if value.startswith("postgresql://"):
            return "postgresql+asyncpg://" + value[len("postgresql://") :]
        if value.startswith("postgresql+psycopg://"):
            return "postgresql+asyncpg://" + value[len("postgresql+psycopg://") :]
        if value.startswith("sqlite:///"):
            return value.replace("sqlite:///", "sqlite+aiosqlite:///", 1)
        return value

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
