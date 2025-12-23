from typing import TYPE_CHECKING, Unpack

from src.application.common.database.receipt_gateway import (
    MultipleReceiptsFilters,
    ReceiptReader,
    ReceiptSaver,
    SingleReceiptFilters,
)

if TYPE_CHECKING:
    from collections.abc import Iterable

    from src.domain.models.receipt import Receipt
    from src.domain.value_objects import ReceiptID


class FakeReceiptGateway(ReceiptReader, ReceiptSaver):
    """
    Dirty receipt gateway
    Better vercion will be done when i will handle how to manage invariants
    """

    def __init__(self, preexisting_receipts: Iterable[Receipt] = []) -> None:
        self.receipts_storage: dict[ReceiptID, Receipt] = {
            receipt.id: receipt for receipt in preexisting_receipts
        }

    async def fetch_receipt(
        self, **filters: Unpack[SingleReceiptFilters]
    ) -> Receipt:
        if filters.get("receipt_id") is not None:
            return self.receipts_storage[filters["receipt_id"]]

        raise NotImplementedError

    async def fetch_receipts(
        self, **filters: Unpack[MultipleReceiptsFilters]
    ) -> list[Receipt]:
        participant_id = filters.get("participant_id")
        return [
            receipt
            for receipt in self.receipts_storage.values()
            if participant_id in receipt.participants_ids
        ]

    async def save_receipt(self, receipt: Receipt) -> None:
        self.receipts_storage[receipt.id] = receipt
