from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.domain.models.user import RealUser


class UserProviderI(Protocol):
    @abstractmethod
    async def fetch_current_user(self) -> RealUser:
        raise NotImplementedError
