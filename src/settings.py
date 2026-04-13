from typing import Annotated

from pydantic import PostgresDsn, RedisDsn, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    DEBUG: bool = False

    DATABASE_DSN: PostgresDsn
    KEY_VALUE_STORE_DSN: RedisDsn

    TELEGRAM_TOKEN: SecretStr
    OPENROUTER_API_KEY: SecretStr

    OCR_MODEL: str
    ASR_MODEL: str
    AGENT_MODEL: str

    RECEIPT_LOCK_PREFIX: str = "receipt_lock"
    RECEIPT_LOCK_LIFETIME: Annotated[int, "seconds"] = 180
