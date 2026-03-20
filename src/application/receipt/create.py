from dataclasses import dataclass
from typing import final

from src.application.common.database.receipt_gateway import (
    ReceiptSaverI,
)
from src.application.common.database.transaction_manager import (
    TransactionManagerI,
)
from src.application.common.interactor import Interactor
from src.application.common.user_provider import UserProviderI
from src.domain.services.receipt import ReceiptService
from src.domain.value_objects import ReceiptID, ReceiptTitle


@dataclass
class CreateReceiptDTO:
    receipt_title: ReceiptTitle


@final
@dataclass(frozen=True)
class CreateReceipt(Interactor[CreateReceiptDTO, ReceiptID]):
    receipt_service: ReceiptService
    receipt_db_gateway: ReceiptSaverI
    user_provider: UserProviderI
    transaction_manager: TransactionManagerI

    async def __call__(self, context: CreateReceiptDTO) -> ReceiptID:
        creditor = await self.user_provider.fetch_current_user()
        receipt = self.receipt_service.create_receipt(
            creditor, context.receipt_title
        )
        await self.receipt_db_gateway.save_receipt(receipt)

        await self.transaction_manager.commit()
        return receipt.id
