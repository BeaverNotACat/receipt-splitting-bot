from collections.abc import AsyncIterable  # noqa: TC003

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.settings import Settings  # noqa: TC001


class AlchemyProvider(Provider):
    scope = Scope.APP

    @provide
    @staticmethod
    def get_alchemy_engine(settings: Settings) -> AsyncEngine:
        return create_async_engine(str(settings.DATABASE_DSN))

    @provide
    @staticmethod
    def get_sqlalchemy_sessionmaker(
        engine: AsyncEngine,
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine)

    @provide(scope=Scope.REQUEST)
    @staticmethod
    async def get_sqlaclhemy_session(
        sessionmaker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession]:
        session = sessionmaker()
        yield session
        await session.close()
