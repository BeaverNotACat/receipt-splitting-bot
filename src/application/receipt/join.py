from dataclasses import dataclass
from typing import final

from src.application.common import Interactor
from src.application.common.database.receipt_gateway import (
    ReceiptGatewayI,  # noqa: TC001
)
from src.application.common.database.transaction_manager import (
    TransactionManagerI,  # noqa: TC001
)
from src.application.common.user_provider import UserProviderI  # noqa: TC001
from src.domain.value_objects import (  # noqa: TC001
    ReceiptID,
)


@dataclass
class JoinReceiptDTO:
    receipt_id: ReceiptID


@final
@dataclass(frozen=True)
class JoinReceipt(Interactor[JoinReceiptDTO, None]):
    user_provider: UserProviderI
    receipt_db_gateway: ReceiptGatewayI
    transaction_manager: TransactionManagerI

    async def __call__(self, context: JoinReceiptDTO) -> None:
        user = await self.user_provider.fetch_current_user()
        receipt = await self.receipt_db_gateway.fetch_receipt(
            id=context.receipt_id
        )
        receipt.append_debtor(user)
        await self.receipt_db_gateway.save_receipt(receipt)
        await self.transaction_manager.commit()
