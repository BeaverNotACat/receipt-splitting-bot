from dataclasses import dataclass
from typing import final

from src.application.common import Interactor
from src.application.common.database import UserSaverI
from src.application.common.database.transaction_manager import (
    TransactionManagerI,
)
from src.application.common.user_provider import UserProviderI
from src.domain.value_objects import (
    UserNickname,
)


@dataclass
class ChangeNicknameDTO:
    nickname: UserNickname


@final
@dataclass(frozen=True)
class ChangeNickname(Interactor[ChangeNicknameDTO, None]):
    transaction_manager: TransactionManagerI
    user_db_gateway: UserSaverI
    user_provider: UserProviderI

    async def __call__(self, context: ChangeNicknameDTO) -> None:
        user = await self.user_provider.fetch_current_user()
        user.nickname = context.nickname
        await self.user_db_gateway.save_user(user)
        await self.transaction_manager.commit()
