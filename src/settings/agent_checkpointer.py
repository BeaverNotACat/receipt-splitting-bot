from typing import Annotated

from pydantic import PostgresDsn
from pydantic_settings import SettingsConfigDict

from .base import Base


class AgentCheckpointerSettings(Base):
    model_config = SettingsConfigDict(env_prefix="CHECKPOINTER_")

    POOL_SIZE: int = 5
    MAX_OVERFLOW: int = 10
    TIMEOUT: Annotated[int, "seconds"] = 30
    DSN: PostgresDsn
