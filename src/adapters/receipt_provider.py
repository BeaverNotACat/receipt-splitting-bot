from typing import TYPE_CHECKING

from src.application.common.database import ReceiptReaderI
from src.application.common.receipt_provider import (
    NoActiveReceiptError,
    ReceiptProviderI,
)

if TYPE_CHECKING:
    from src.domain.models.receipt import Receipt
    from src.domain.value_objects import ReceiptID


class ReceiptProvider(ReceiptProviderI):
    def __init__(
        self, receipt_reader: ReceiptReaderI, receipt_id: ReceiptID | None
    ) -> None:
        self.receipt_reader = receipt_reader
        self.receipt_id = receipt_id

    async def fetch_current_receipt(self) -> Receipt:
        if self.receipt_id is None:
            raise NoActiveReceiptError

        # TODO(beavernotacat): Potential security issue
        # https://github.com/BeaverNotACat/receipt-splitting-bot/issues/47
        return await self.receipt_reader.fetch_receipt(id=self.receipt_id)
