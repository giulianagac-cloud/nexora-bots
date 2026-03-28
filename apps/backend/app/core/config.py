from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TRENBOT_", extra="ignore")

    app_name: str = "TrenBot Enterprise Backend"
    environment: str = Field(default="development")
    api_prefix: str = "/"
    client_id: str = Field(default="demo")


@lru_cache
def get_settings() -> Settings:
    return Settings()

