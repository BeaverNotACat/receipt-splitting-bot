from pydantic import RedisDsn
from pydantic_settings import SettingsConfigDict

from .base import Base


class KeyValueSettings(Base):
    model_config = SettingsConfigDict(env_prefix="KEY_VALUE_")

    DSN: RedisDsn
