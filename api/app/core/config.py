from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "KRI Dashboard API"
    app_env: str = "dev"
    api_prefix: str = "/api"
    secret_key: str = "change-me"
    access_token_expires_minutes: int = 480
    algorithm: str = "HS256"
    database_url: str = "postgresql+psycopg://kri:kri@db:5432/kri_dashboard"
    admin_username: str = "admin"
    admin_password: str = "admin123"
    demo_stale: bool = False
    seed_enabled: bool = True
    cors_origins: str = "http://localhost:3000"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


@lru_cache
def get_settings() -> Settings:
    return Settings()
