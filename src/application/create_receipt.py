from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, final

from src.application.common.database.receipt_gateway import ReceiptSaver
from src.application.common.database.user_gateway import UserReader
from src.application.common.interactor import Interactor
from src.domain.value_objects import ChatID, ReceiptID

if TYPE_CHECKING:
    from src.domain.services.receipt import ReceiptService


class ReceiptDBGateway(ReceiptSaver, Protocol): ...


class UserDBGateway(UserReader, Protocol): ...


@dataclass
class CreateReceiptDTO:
    chat_id: ChatID
    receipt_title: str


@final
@dataclass(frozen=True)
class CreateReceipt(Interactor[CreateReceiptDTO, ReceiptID]):
    receipt_service: ReceiptService
    receipt_db_gateway: ReceiptDBGateway
    user_db_gateway: UserDBGateway

    async def __call__(self, context: CreateReceiptDTO) -> ReceiptID:
        creditor = await self.user_db_gateway.fetch_real_user(
            chat_id=context.chat_id
        )
        receipt = self.receipt_service.create_receipt(
            creditor, context.receipt_title
        )
        await self.receipt_db_gateway.save_receipt(receipt)
        return receipt.id
