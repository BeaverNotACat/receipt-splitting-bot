from dataclasses import dataclass

from src.domain.value_objects import (  # noqa: TC001
    ChatID,
    UserID,
    UserNickname,
)


@dataclass
class _BaseUser:
    id: UserID
    nickname: UserNickname


@dataclass
class DummyUser(_BaseUser): ...


@dataclass
class RealUser(_BaseUser):
    chat_id: ChatID


User = DummyUser | RealUser
