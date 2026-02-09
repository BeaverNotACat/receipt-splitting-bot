from dataclasses import dataclass  # noqa: I001
from typing import final

from src.application.common.database.receipt_gateway import ReceiptSaverI  # noqa: TC001
from src.application.common.interactor import Interactor
from src.domain.services.receipt import ReceiptService  # noqa: TC001
from src.domain.value_objects import ReceiptID, ReceiptTitle
from src.application.common.user_provider import UserProviderI  # noqa: TC001


@dataclass
class CreateReceiptDTO:
    receipt_title: ReceiptTitle


@final
@dataclass(frozen=True)
class CreateReceipt(Interactor[CreateReceiptDTO, ReceiptID]):
    receipt_service: ReceiptService
    receipt_db_gateway: ReceiptSaverI
    user_provider: UserProviderI

    async def __call__(self, context: CreateReceiptDTO) -> ReceiptID:
        creditor = await self.user_provider.fetch_current_user()
        receipt = self.receipt_service.create_receipt(
            creditor, context.receipt_title
        )
        await self.receipt_db_gateway.save_receipt(receipt)
        return receipt.id
