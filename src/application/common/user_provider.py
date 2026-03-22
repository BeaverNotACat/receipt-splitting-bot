from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.domain.models.user import RealUser


class NoActiveUserError(Exception): ...


class UserProviderI(Protocol):
    """
    Port for identifying current user
    """

    @abstractmethod
    async def fetch_current_user(self) -> RealUser:
        """
        Obtains current user thru presentation layer context

        Raises:
            NoActiveUserError: If user is not signed up/in
        """
        raise NotImplementedError
