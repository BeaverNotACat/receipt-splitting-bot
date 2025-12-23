from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Protocol, final

from src.application.common import Interactor
from src.application.common.database import UserSaver
from src.application.common.database.receipt_gateway import (
    ReceiptReader,
    ReceiptSaver,
)
from src.domain.value_objects import (  # noqa: TC001
    ChatID,
    ReceiptID,
    UserNickname,
)

if TYPE_CHECKING:
    from src.domain.models import RealUser
    from src.domain.services import UserService


class UserDBGateway(UserSaver, Protocol): ...


class ReceiptDBGateway(ReceiptReader, ReceiptSaver, Protocol): ...


_sentinel: Any = object()


@dataclass
class OnboardUserDTO:
    chat_id: ChatID
    nickname: UserNickname
    receipt_id: ReceiptID = _sentinel


@final
@dataclass(frozen=True)
class OnboardUser(Interactor[OnboardUserDTO, None]):
    user_service: UserService
    user_db_gateway: UserDBGateway
    receipt_db_gateway: ReceiptDBGateway

    async def __call__(self, context: OnboardUserDTO) -> None:
        user = await self.register_user(context.chat_id, context.nickname)
        if context.receipt_id is not _sentinel:
            await self.add_to_receipt(user, context.receipt_id)

    async def register_user(
        self, chat_id: ChatID, nickname: UserNickname
    ) -> RealUser:
        user = self.user_service.create_real_user(chat_id, nickname)
        await self.user_db_gateway.save_user(user)
        return user

    async def add_to_receipt(
        self, user: RealUser, receipt_id: ReceiptID
    ) -> None:
        receipt = await self.receipt_db_gateway.fetch_receipt(
            receipt_id=receipt_id
        )
        receipt.append_debtor(user)
        await self.receipt_db_gateway.save_receipt(receipt)
