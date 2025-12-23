from typing import TYPE_CHECKING

from src.application.common.user_provider import UserProvider

if TYPE_CHECKING:
    from src.domain.models.user import RealUser


class FakeUserProvider(UserProvider):
    def __init__(self, user: RealUser) -> None:
        self.user = user

    async def fetch_current_user(self) -> RealUser:
        return self.user
