from typing import TYPE_CHECKING, ClassVar, Unpack

from src.application.common.database.user_gateway import (
    UserFilters,
    UserReader,
    UserSaver,
)
from src.domain.models.user import RealUser, User
from src.domain.value_objects import UserID

if TYPE_CHECKING:
    from collections.abc import Iterable


class FakeUserGateway(UserReader, UserSaver):
    """
    Dirty user gateway
    Better version will be done when i will handle how to manage invariants
    """

    users_storage: dict[UserID, User]

    def __init__(self, preexisting_users: Iterable[User] = []) -> None:
        self.users_storage = {user.id: user for user in preexisting_users}

    async def fetch_user(self, **filters: Unpack[UserFilters]) -> User:
        if filters.get("user_id") is not None:
            return self.users_storage[filters["user_id"]]

        if filters.get("chat_id") is not None:
            for user in self.users_storage.values():
                if (
                    isinstance(user, RealUser)
                    and user.chat_id == filters["chat_id"]
                ):
                    return user

        raise NotImplementedError

    async def save_user(self, user: User) -> None:
        self.users_storage[user.id] = user
