from abc import abstractmethod
from collections.abc import Sequence
from typing import (
    TYPE_CHECKING,
    Protocol,
    TypedDict,
    Unpack,
)

from src.domain.value_objects import ChatID, UserID

if TYPE_CHECKING:
    from src.domain.models.user import User


class UserFilters(TypedDict, total=False):
    id: UserID
    chat_id: ChatID


class MultipleUsersFilters(TypedDict, total=False):
    ids: Sequence[UserID]


class UserNotFoundError(Exception): ...


class UserReaderI(Protocol):
    @abstractmethod
    async def fetch_user(self, **filters: Unpack[UserFilters]) -> User:
        raise NotImplementedError

    @abstractmethod
    async def fetch_users(
        self, **filters: Unpack[MultipleUsersFilters]
    ) -> list[User]:
        raise NotImplementedError


class UserSaverI(Protocol):
    @abstractmethod
    async def save_user(self, user: User) -> None:
        raise NotImplementedError


class UserGatewayI(UserReaderI, UserSaverI, Protocol): ...
