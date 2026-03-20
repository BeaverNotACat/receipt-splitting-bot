from dataclasses import dataclass
from typing import final

from src.application.common.database.receipt_gateway import (
    ReceiptReaderI,
)
from src.application.common.interactor import Interactor
from src.application.common.user_provider import UserProviderI
from src.domain.models.receipt import Receipt
from src.domain.value_objects import LimitOffsetPagination


@dataclass(frozen=True)
class ListReceiptsDTO:
    pagination: LimitOffsetPagination


@dataclass(frozen=True)
class ListReceiptsResultDTO:
    receipts: list[Receipt]
    total: int


@final
@dataclass(frozen=True)
class ListReceipts(Interactor[ListReceiptsDTO, ListReceiptsResultDTO]):
    user_provider: UserProviderI
    receipt_db_gateway: ReceiptReaderI

    async def __call__(
        self, context: ListReceiptsDTO
    ) -> ListReceiptsResultDTO:
        user = await self.user_provider.fetch_current_user()
        return ListReceiptsResultDTO(
            receipts=await self.receipt_db_gateway.fetch_receipts(
                pagination=context.pagination, participant_id=user.id
            ),
            total=await self.receipt_db_gateway.count_receipts(
                participant_id=user.id
            ),
        )
