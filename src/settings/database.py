from pydantic import PostgresDsn
from pydantic_settings import SettingsConfigDict

from .base import Base


class DatabaseSettings(Base):
    model_config = SettingsConfigDict(env_prefix="DATABASE_")

    DSN: PostgresDsn
