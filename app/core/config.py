from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configurações da aplicação."""

    PROJECT_NAME: str = "Template FastAPI"
    APP_NAME: str = "Template FastAPI API"
    APP_VERSION: str = "0.1.0"
    ENVIRONMENT: str = "development"
    API_V1_STR: str = "/api/v1"
    DEBUG: bool = False

    ORIGINS: list[str] = [
        "http://localhost:8000",
        "http://localhost:3000",
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000",
    ]

    DATABASE_URL: str = "sqlite:///./sql_app.db"
    DATABASE_TEST_URL: str = "sqlite:///./test.db"

    SECRET_KEY: str = "seu_secret_key_muito_seguro_aqui_mude_em_producao"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    @model_validator(mode="after")
    def validate_secret_key_for_production(self) -> "Settings":
        insecure_default = "seu_secret_key_muito_seguro_aqui_mude_em_producao"
        if self.ENVIRONMENT.lower() == "production" and self.SECRET_KEY == insecure_default:
            raise ValueError("SECRET_KEY padrão não pode ser usado em produção")
        return self


settings = Settings()
