from dataclasses import dataclass  # noqa: I001
from typing import final

from src.application.common.database.receipt_gateway import (
    ReceiptGatewayI,
)
from src.application.common.database.user_gateway import UserSaverI
from src.application.common.interactor import Interactor
from src.domain.value_objects import ReceiptID, UserID, UserNickname

from src.application.common.user_provider import UserProviderI
from src.domain.services.user import UserService


@dataclass
class AddDummyUserDTO:
    receipt_id: ReceiptID
    nickname: UserNickname


@final
@dataclass(frozen=True)
class AddDummyUser(Interactor[AddDummyUserDTO, UserID]):
    user_provider: UserProviderI
    user_service: UserService
    receipt_db_gateway: ReceiptGatewayI
    user_db_gateway: UserSaverI

    async def __call__(self, context: AddDummyUserDTO) -> UserID:
        dummy = self.user_service.create_dummy_user(context.nickname)
        receipt = await self.receipt_db_gateway.fetch_receipt(
            id=context.receipt_id
        )
        receipt.append_debtor(dummy)

        await self.user_db_gateway.save_user(dummy)
        await self.receipt_db_gateway.save_receipt(receipt)

        return dummy.id
