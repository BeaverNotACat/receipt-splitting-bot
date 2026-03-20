from dataclasses import dataclass
from typing import final

from src.application.common.database.receipt_gateway import (
    ReceiptReaderI,
)
from src.application.common.interactor import Interactor
from src.application.common.user_provider import UserProviderI
from src.domain.models.receipt import Receipt


@final
@dataclass(frozen=True)
class ListReceipts(Interactor[None, list[Receipt]]):
    user_provider: UserProviderI
    receipt_db_gateway: ReceiptReaderI

    async def __call__(self, context: None) -> list[Receipt]:  # noqa: ARG002
        user = await self.user_provider.fetch_current_user()
        return await self.receipt_db_gateway.fetch_receipts(
            participant_id=user.id
        )
