from typing import Annotated

from pydantic_settings import SettingsConfigDict

from .base import Base


class ReceiptLockSettings(Base):
    model_config = SettingsConfigDict(env_prefix="RECEIPT_LOCK_")

    PREFIX: str = "receipt_lock"
    LIFETIME: Annotated[int, "seconds"] = 180
