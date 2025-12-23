from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, final

from src.application.common.database.receipt_gateway import ReceiptReader
from src.application.common.interactor import Interactor
from src.domain.models.receipt import Receipt

if TYPE_CHECKING:
    from src.application.common.user_provider import UserProvider


class ReceiptDBGateway(ReceiptReader, Protocol): ...


@final
@dataclass(frozen=True)
class ListReceipts(Interactor[None, list[Receipt]]):
    user_provider: UserProvider
    receipt_db_gateway: ReceiptDBGateway

    async def __call__(self, context: None) -> list[Receipt]:  # noqa: ARG002
        user = await self.user_provider.fetch_current_user()
        return await self.receipt_db_gateway.fetch_receipts(
            participant_id=user.id
        )
