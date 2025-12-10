from uuid import uuid7

from src.domain.models.user import DummyUser, RealUser
from src.domain.value_objects import ChatID, UserID


class UserService:
    @staticmethod
    def create_real_user(chat_id: ChatID, name: str) -> RealUser:
        return RealUser(
            id=UserID(uuid7()),
            name=name,
            chat_id=chat_id,
        )

    @staticmethod
    def create_dummy_user(name: str) -> DummyUser:
        return DummyUser(
            id=UserID(uuid7()),
            name=name,
        )
