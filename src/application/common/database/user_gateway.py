from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, TypedDict, Unpack

from src.domain.value_objects import ChatID, UserID  # noqa: TC001

if TYPE_CHECKING:
    from src.domain.models.user import RealUser, User


class UserFilters(TypedDict, total=False):
    user_id: UserID
    chat_id: ChatID


class UserReader(Protocol):
    @abstractmethod
    async def fetch_user(self, **filters: Unpack[UserFilters]) -> User:
        raise NotImplementedError

    @abstractmethod
    async def fetch_real_user(
        self, **filters: Unpack[UserFilters]
    ) -> RealUser:
        raise NotImplementedError


class UserSaver(Protocol):
    @abstractmethod
    async def save_user(self, user: User) -> None:
        raise NotImplementedError
