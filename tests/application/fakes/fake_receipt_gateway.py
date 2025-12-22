from typing import TYPE_CHECKING, Unpack

from src.application.common.database.receipt_gateway import (
    ReceiptFilters,
    ReceiptReader,
    ReceiptSaver,
)

if TYPE_CHECKING:
    from collections.abc import Iterable

    from src.domain.models.receipt import Receipt


class FakeReceiptGateway(ReceiptReader, ReceiptSaver):
    """
    Dirty receipt gateway
    Better vercion will be done when i will handle how to manage invariants
    """

    def __init__(self, preexisting_receipts: Iterable[Receipt] = []) -> None:
        self.receipts_storage = {
            receipt.id: receipt for receipt in preexisting_receipts
        }

    async def fetch_receipt(
        self, **filters: Unpack[ReceiptFilters]
    ) -> Receipt:
        if filters.get("receipt_id") is not None:
            return self.receipts_storage[filters["receipt_id"]]

        raise NotImplementedError

    async def save_receipt(self, receipt: Receipt) -> None:
        self.receipts_storage[receipt.id] = receipt
