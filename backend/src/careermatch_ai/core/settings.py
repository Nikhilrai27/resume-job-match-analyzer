from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "CareerMatch AI"
    environment: str = "development"
    api_v1_prefix: str = "/api/v1"
    secret_key: str = Field(default="change-me", alias="SECRET_KEY")
    access_token_expire_minutes: int = 60
    database_url: str = Field(
        default="postgresql+psycopg://careermatch:careermatch@db:5432/careermatch",
        alias="DATABASE_URL",
    )
    google_client_id: str = Field(default="google-client-id", alias="GOOGLE_CLIENT_ID")
    google_client_secret: str = Field(default="google-client-secret", alias="GOOGLE_CLIENT_SECRET")
    frontend_url: str = Field(default="http://localhost:3000", alias="FRONTEND_URL")
    groq_api_key: str = Field(default="", alias="GROQ_API_KEY")
    gemini_api_key: str = Field(default="", alias="GEMINI_API_KEY")
    openai_api_key: str = Field(default="", alias="OPENAI_API_KEY")
    groq_model: str = Field(default="llama-3.3-70b-versatile", alias="GROQ_MODEL")
    gemini_model: str = Field(default="gemini-2.0-flash", alias="GEMINI_MODEL")
    openai_model: str = Field(default="gpt-4o-mini", alias="OPENAI_MODEL")
    profiles_dir: Path = Field(default=Path(__file__).resolve().parents[4] / "company_profiles")
    upload_dir: Path = Field(default=Path(__file__).resolve().parents[4] / "storage")

    model_config = SettingsConfigDict(env_file=".env", extra="ignore", populate_by_name=True)


@lru_cache
def get_settings() -> Settings:
    return Settings()
