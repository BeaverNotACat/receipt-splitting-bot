from typing import Unpack

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: TC002

from src.application.common.database.user_gateway import (
    UserFilters,
    UserNotFoundError,
    UserReaderI,
    UserSaverI,
)
from src.domain.models.user import DummyUser, RealUser, User
from src.domain.value_objects import ChatID, UserID, UserNickname

from .orm import UserORM


class UserGateway(UserReaderI, UserSaverI):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def fetch_user(self, **filters: Unpack[UserFilters]) -> User:
        query = select(UserORM).filter_by(**filters)
        user_orm = await self.session.execute(query)
        try:
            return self._map_to_domain(user_orm.scalar_one())
        except NoResultFound:
            raise UserNotFoundError from NoResultFound

    async def save_user(self, user: User) -> None:
        user_orm = self._map_to_orm(user)
        await self.session.merge(user_orm)

    @staticmethod
    def _map_to_domain(orm: UserORM) -> User:
        if orm.chat_id is None:
            return DummyUser(
                id=UserID(orm.id),
                nickname=UserNickname(orm.nickname),
            )
        return RealUser(
            id=UserID(orm.id),
            nickname=(UserNickname(orm.nickname)),
            chat_id=ChatID(orm.chat_id),
        )

    @staticmethod
    def _map_to_orm(model: User) -> UserORM:
        return UserORM(
            id=model.id,
            nickname=model.nickname,
            chat_id=getattr(model, "chat_id"),  # noqa: B009
        )
