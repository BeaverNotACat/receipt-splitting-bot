from abc import abstractmethod
from typing import TYPE_CHECKING, Protocol, TypedDict, Unpack

from src.domain.value_objects import ReceiptID, UserID  # noqa: TC001

if TYPE_CHECKING:
    from src.domain.models.receipt import Receipt


class SingleReceiptFilters(TypedDict, total=False):
    receipt_id: ReceiptID


class MultipleReceiptsFilters(TypedDict, total=False):
    participant_id: UserID


class ReceiptReader(Protocol):
    @abstractmethod
    async def fetch_receipt(
        self, **filters: Unpack[SingleReceiptFilters]
    ) -> Receipt:
        raise NotImplementedError

    @abstractmethod
    async def fetch_receipts(
        self, **filters: Unpack[MultipleReceiptsFilters]
    ) -> list[Receipt]:
        raise NotImplementedError


class ReceiptSaver(Protocol):
    @abstractmethod
    async def save_receipt(self, receipt: Receipt) -> None:
        raise NotImplementedError
