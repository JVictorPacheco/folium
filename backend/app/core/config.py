from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_name: str = "Folium API"
    environment: str = "development"
    database_url: str = "postgresql+asyncpg://folium:folium@localhost:5432/folium"
    jwt_secret_key: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 60 * 24 * 7
    storage_dir: str = "./storage"
    media_url_prefix: str = "/media"
    max_image_bytes: int = 10 * 1024 * 1024
    max_pdf_bytes: int = 25 * 1024 * 1024
    reset_token_expire_minutes: int = 60
    frontend_url: str = "http://localhost:5173"
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_username: str = ""
    smtp_password: str = ""
    smtp_from_email: str = "Folium <no-reply@folium.app>"
    smtp_use_tls: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
