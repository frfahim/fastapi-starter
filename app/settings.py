import secrets
from functools import lru_cache

from pydantic import BaseModel, PostgresDsn, SecretStr, AnyHttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict


class Security(BaseModel):
    JWT_ISSUER: str = "my-app"
    JWT_SECRET_KEY: SecretStr
    ACCESS_TOKEN_LIFETIME: int = 1800  # 30 min
    REFRESH_TOKEN_LIFETIME: int = 24 * 3600  # 1d
    ALLOWED_HOST: list[str] = ["localhost", "127.0.0.1"]
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []


class Settings(BaseSettings):
    # security: Security
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True, extra="ignore")

    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    POSTGRES_URL: PostgresDsn

    SECRET_KEY: str = secrets.token_urlsafe(32)
    ALGORITHM: str = "HS256"
    # ACCESS_TOKEN_EXPIRE_MINUTES: int = 3600
    DATE_FORMAT: str = "%Y-%m-%d"

    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Starter API Docs"
    APP_VERSION: str


@lru_cache
def get_settings():
    return Settings()  # type: ignore


settings = get_settings()
