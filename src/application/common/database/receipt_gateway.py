from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, TypedDict, Unpack

from src.domain.value_objects import ReceiptID  # noqa: TC001

if TYPE_CHECKING:
    from src.domain.models.receipt import Receipt


class ReceiptFilters(TypedDict):
    receipt_id: ReceiptID


class ReceiptReader(Protocol):
    @abstractmethod
    async def fetch_receipt(
        self, **filters: Unpack[ReceiptFilters]
    ) -> Receipt:
        raise NotImplementedError


class ReceiptSaver(Protocol):
    @abstractmethod
    async def save_receipt(self, receipt: Receipt) -> None:
        raise NotImplementedError
