from collections.abc import AsyncGenerator, AsyncIterable

from dishka import Provider, Scope, provide
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.adapters.database import UserGateway
from src.adapters.database.receipt_gateway import ReceiptGateway
from src.application.onboard import (
    OnboardUser,
    ReceiptDBGateway,
    UserDBGateway,
)
from src.domain.services import ReceiptService, UserService
from src.settings import Settings


class DIProvider(Provider):
    scope = Scope.REQUEST

    @provide(scope=Scope.APP)
    def get_settings(self) -> Settings:
        return Settings()

    @provide(scope=Scope.APP)
    def get_sqlalchemy_engine(self, settings: Settings) -> AsyncEngine:
        return create_async_engine(str(settings.DATABASE_DSN))

    @provide(scope=Scope.APP)
    def get_sqlalchemy_sessionmaker(
        self, engine: AsyncEngine
    ) -> async_sessionmaker[AsyncSession]:
        return async_sessionmaker(engine)

    @provide
    async def get_sqlaclhemy_session(
        self, sessionmaker: async_sessionmaker[AsyncSession]
    ) -> AsyncIterable[AsyncSession]:
        session = sessionmaker()
        yield session
        await session.close()

    user_service = provide(UserService)
    receipt_service = provide(ReceiptService)

    user_reader = provide(UserGateway, provides=UserDBGateway)
    receipt_reader = provide(ReceiptGateway, provides=ReceiptDBGateway)

    onboard_interactor = provide(OnboardUser)
