from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

from .base import Base


class TelegramSettings(Base):
    model_config = SettingsConfigDict(env_prefix="TELEGRAM_")

    TOKEN: SecretStr
