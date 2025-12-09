from uuid import uuid7

from src.domain.models.user import DummyUser, RealUser
from src.domain.value_objects import UserID


def create_real_user(telegram_id: int, name: str) -> RealUser:
    return RealUser(
        id=UserID(uuid7()),
        name=name,
        telegram_id=telegram_id,
    )


def create_dummy_user(name: str) -> DummyUser:
    return DummyUser(
        id=UserID(uuid7()),
        name=name,
    )
