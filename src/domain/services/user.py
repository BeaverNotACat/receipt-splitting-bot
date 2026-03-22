from typing import TYPE_CHECKING
from uuid import uuid7

from src.domain.models.user import BaseUserData, DummyUser, RealUser
from src.domain.value_objects import ChatID, UserID, UserNickname

if TYPE_CHECKING:
    from src.domain.models.user import User


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

    @staticmethod
    def narrow_to_basic_user_data(user: User) -> BaseUserData:
        return BaseUserData(user.id, user.nickname)
