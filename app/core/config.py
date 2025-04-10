from typing import Optional, Dict, Any

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação."""

    # Configurações gerais
    PROJECT_NAME: str = "Template FastAPI"
    APP_NAME: str = "Template FastAPI API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = True

    # Configurações CORS
    ORIGINS: list[str] = ["http://localhost:8000", "http://localhost:3000",
                          "http://127.0.0.1:8000", "http://127.0.0.1:3000"]

    # Configurações de banco de dados
    DATABASE_URL: str = "sqlite:///./sql_app.db"
    DATABASE_TEST_URL: str = "sqlite:///./test.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )


settings = Settings()
