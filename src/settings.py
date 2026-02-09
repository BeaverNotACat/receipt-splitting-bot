from pydantic import PostgresDsn, SecretStr  # noqa: TC002
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    TELEGRAM_TOKEN: SecretStr
    DATABASE_DSN: PostgresDsn
