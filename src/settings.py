from pydantic import PostgresDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DEBUG: bool = False

    DATABASE_DSN: PostgresDsn

    TELEGRAM_TOKEN: SecretStr
    OPENROUTER_API_KEY: SecretStr

    OCR_MODEL: str
    ASR_MODEL: str
    AGENT_MODEL: str
