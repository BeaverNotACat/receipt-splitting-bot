from typing import cast

from src.application.common.database.user_gateway import (
    UserNotFoundError,
    UserReaderI,
)
from src.application.common.user_provider import (
    UserIsNotRegisteredError,
    UserProviderI,
)
from src.domain.models.user import RealUser
from src.domain.value_objects import ChatID


class UserProvider(UserProviderI):
    def __init__(
        self, user_reader: UserReaderI, chat_id: ChatID | None
    ) -> None:
        self.user_reader = user_reader
        self.chat_id = chat_id

    async def fetch_current_user(self) -> RealUser:
        if self.chat_id is None:
            raise UserIsNotRegisteredError
        try:
            return cast(
                "RealUser",
                await self.user_reader.fetch_user(chat_id=self.chat_id),
            )
        except UserNotFoundError:
            raise UserIsNotRegisteredError from UserNotFoundError
