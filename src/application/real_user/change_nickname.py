from dataclasses import dataclass
from typing import final

from src.application.common import Interactor
from src.application.common.database import UserReaderI, UserSaverI
from src.application.common.database.transaction_manager import (
    TransactionManagerI,
)
from src.domain.value_objects import (
    ChatID,
    UserNickname,
)


@dataclass
class ChangeNicknameDTO:
    chat_id: ChatID
    nickname: UserNickname


@final
@dataclass(frozen=True)
class ChangeNickname(Interactor[ChangeNicknameDTO, None]):
    transaction_manager: TransactionManagerI
    user_reader_saver: UserReaderI | UserSaverI

    async def __call__(self, context: ChangeNicknameDTO) -> None:
        user = await self.user_reader_saver.fetch_user(chat_id=context.chat_id)
        user.nickname = context.nickname
        await self.user_reader_saver.save_user(user)
        await self.transaction_manager.commit()
