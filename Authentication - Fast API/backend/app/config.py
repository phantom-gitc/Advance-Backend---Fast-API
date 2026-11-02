from pathlib import Path
from dotenv import load_dotenv
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Locate and load the .env file using python-dotenv
BASE_DIR = Path(__file__).resolve().parent.parent
env_path = BASE_DIR / ".env"
load_dotenv(dotenv_path=env_path)


class Settings(BaseSettings):
    # MongoDB settings
    MONGO_URI: str
    DATABASE_NAME: str = "fastapi_auth"

    # JWT secrets and token lifetime
    ACCESS_TOKEN_SECRET: str
    REFRESH_TOKEN_SECRET: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    JWT_ALGORITHM: str = "HS256"

    # Cookie settings
    COOKIE_SECURE: bool = False
    COOKIE_SAMESITE: str = "lax"
    COOKIE_DOMAIN: str | None = None

    # CORS and environment
    FRONTEND_URL: str = "http://localhost:5173"
    ENVIRONMENT: str = "development"

    @field_validator("COOKIE_DOMAIN", mode="before")
    @classmethod
    def empty_str_to_none(cls, v):
        # If COOKIE_DOMAIN is empty in .env, treat it as None
        if isinstance(v, str) and not v.strip():
            return None
        return v

    model_config = SettingsConfigDict(
        env_file=env_path,
        env_file_encoding="utf-8",
        extra="ignore",
    )


# Single loaded settings instance
settings = Settings()
