from pydantic import PostgresDsn
from pydantic_settings import SettingsConfigDict

from .base import Base


class AgentCheckpointerSettings(Base):
    model_config = SettingsConfigDict(env_prefix="CHECKPOINTER_")

    DSN: PostgresDsn | None = None
