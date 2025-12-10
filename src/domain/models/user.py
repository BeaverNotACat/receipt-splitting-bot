from dataclasses import dataclass

from src.domain.value_objects import ChatID, UserID  # noqa: TC001


@dataclass
class _BaseUser:
    id: UserID
    name: str


@dataclass
class DummyUser(_BaseUser): ...


@dataclass
class RealUser(_BaseUser):
    chat_id: ChatID


User = DummyUser | RealUser
