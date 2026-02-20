from dataclasses import dataclass
from typing import final

from src.application.common.database.receipt_gateway import (
    ReceiptReaderI,
)
from src.application.common.interactor import Interactor
from src.domain.models.receipt import Receipt
from src.domain.value_objects import ReceiptID


@dataclass
class GetReceiptDTO:
    receipt_id: ReceiptID


@final
@dataclass(frozen=True)
class GetReceipt(Interactor[GetReceiptDTO, Receipt]):
    receipt_db_gateway: ReceiptReaderI

    async def __call__(self, context: GetReceiptDTO) -> Receipt:
        return await self.receipt_db_gateway.fetch_receipt(
            id=context.receipt_id
        )
