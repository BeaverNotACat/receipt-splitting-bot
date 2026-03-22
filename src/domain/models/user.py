from dataclasses import dataclass

from src.domain.value_objects import (
    ChatID,
    UserID,
    UserNickname,
)


@dataclass
class BaseUserData:
    id: UserID
    nickname: UserNickname


@dataclass
class DummyUser(BaseUserData): ...


@dataclass
class RealUser(BaseUserData):
    chat_id: ChatID


User = DummyUser | RealUser
