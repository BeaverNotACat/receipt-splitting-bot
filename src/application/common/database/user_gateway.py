from abc import abstractmethod
from typing import (
    TYPE_CHECKING,
    Protocol,
    TypedDict,
    Unpack,
)

from src.domain.value_objects import ChatID, UserID  # noqa: TC001

if TYPE_CHECKING:
    from src.domain.models.user import User


class UserFilters(TypedDict, total=False):
    id: UserID
    chat_id: ChatID


class UserReaderI(Protocol):
    @abstractmethod
    async def fetch_user(self, **filters: Unpack[UserFilters]) -> User:
        raise NotImplementedError


class UserSaverI(Protocol):
    @abstractmethod
    async def save_user(self, user: User) -> None:
        raise NotImplementedError


class UserGatewayI(UserReaderI, UserSaverI, Protocol): ...
