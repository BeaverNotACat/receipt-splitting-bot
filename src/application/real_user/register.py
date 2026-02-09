from dataclasses import dataclass
from typing import final

from src.application.common import Interactor
from src.application.common.database import UserSaverI  # noqa: TC001
from src.application.common.database.transaction_manager import (
    TransactionManagerI,  # noqa: TC001
)
from src.domain.services import UserService  # noqa: TC001
from src.domain.value_objects import (
    ChatID,
    UserID,
    UserNickname,
)


@dataclass
class RegisterUserDTO:
    chat_id: ChatID
    nickname: UserNickname


@final
@dataclass(frozen=True)
class RegisterUser(Interactor[RegisterUserDTO, UserID]):
    transaction_manager: TransactionManagerI
    user_service: UserService
    user_db_gateway: UserSaverI

    async def __call__(self, context: RegisterUserDTO) -> UserID:
        user = self.user_service.create_real_user(
            context.chat_id, context.nickname
        )
        await self.user_db_gateway.save_user(user)
        await self.transaction_manager.commit()
        return user.id
