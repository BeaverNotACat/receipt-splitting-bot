from pydantic import SecretStr
from pydantic_settings import SettingsConfigDict

from .base import Base


class OpenRouterSettings(Base):
    model_config = SettingsConfigDict(env_prefix="OPENROUTER_")

    API_KEY: SecretStr

    OCR_MODEL: str
    ASR_MODEL: str
    AGENT_MODEL: str
