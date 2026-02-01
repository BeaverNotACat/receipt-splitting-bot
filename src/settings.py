from pydantic import PostgresDsn  # noqa: TC002
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_DSN: PostgresDsn
