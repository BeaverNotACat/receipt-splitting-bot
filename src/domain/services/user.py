from uuid import uuid7

from src.domain.models.user import DummyUser, RealUser
from src.domain.value_objects import ChatID, UserID, UserNickname


class UserService:
    @staticmethod
    def create_real_user(chat_id: ChatID, nickname: UserNickname) -> RealUser:
        return RealUser(
            id=UserID(uuid7()),
            nickname=nickname,
            chat_id=chat_id,
        )

    @staticmethod
    def create_dummy_user(nickname: UserNickname) -> DummyUser:
        return DummyUser(
            id=UserID(uuid7()),
            nickname=nickname,
        )
