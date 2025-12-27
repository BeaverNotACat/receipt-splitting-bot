from dataclasses import dataclass
from typing import TYPE_CHECKING, Protocol, final

from src.application.common.database.receipt_gateway import (
    ReceiptReader,
    ReceiptSaver,
)
from src.application.common.database.user_gateway import UserSaver
from src.application.common.interactor import Interactor
from src.domain.value_objects import ReceiptID, UserID, UserNickname

if TYPE_CHECKING:
    from src.application.common.user_provider import UserProvider
    from src.domain.services.user import UserService


class UserDBGateway(UserSaver, Protocol): ...


class ReceiptDBGateway(ReceiptSaver, ReceiptReader, Protocol): ...


@dataclass
class AddDummyUserDTO:
    receipt_id: ReceiptID
    nickname: UserNickname


@final
@dataclass(frozen=True)
class AddDummyUser(Interactor[AddDummyUserDTO, UserID]):
    user_provider: UserProvider
    user_service: UserService
    receipt_db_gateway: ReceiptDBGateway
    user_db_gateway: UserDBGateway

    async def __call__(self, context: AddDummyUserDTO) -> UserID:
        dummy = self.user_service.create_dummy_user(context.nickname)
        receipt = await self.receipt_db_gateway.fetch_receipt(
            receipt_id=context.receipt_id
        )
        receipt.append_debtor(dummy)

        await self.user_db_gateway.save_user(dummy)
        await self.receipt_db_gateway.save_receipt(receipt)

        return dummy.id
