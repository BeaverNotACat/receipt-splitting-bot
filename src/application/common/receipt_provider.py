from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol

if TYPE_CHECKING:
    from src.domain.models import Receipt


class NoActiveReceiptError(Exception): ...


class ReceiptProviderI(Protocol):
    """
    Port for identifying user's opened receipt
    """

    @abstractmethod
    async def fetch_current_receipt(self) -> Receipt:
        """
        Obtains current receipt thru presentation layer context

        Raises:
            NoActiveReceiptError: If user dont have any receipt opened
        """
        raise NotImplementedError
