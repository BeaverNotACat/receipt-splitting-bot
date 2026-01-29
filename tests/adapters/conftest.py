import asyncio
from typing import TYPE_CHECKING

import pytest
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from src.adapters.database.receipt_gateway import ReceiptGateway
from src.adapters.database.user_gateway import UserGateway
from src.settings import Settings

if TYPE_CHECKING:
    from collections.abc import Generator


@pytest.fixture(scope="session")
def settings() -> Settings:
    return Settings()


@pytest.fixture(scope="session")
def sqlalchemy_engine(settings: Settings) -> AsyncEngine:
    return create_async_engine(str(settings.DATABASE_DSN))


@pytest.fixture(scope="session")
def sqlalchemy_sessionmaker(
    sqlalchemy_engine: AsyncEngine,
) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(sqlalchemy_engine)


@pytest.fixture
def sqlalchemy_session(
    sqlalchemy_sessionmaker: async_sessionmaker[AsyncSession],
) -> Generator[AsyncSession]:
    session = sqlalchemy_sessionmaker()
    yield session
    asyncio.run(session.close())


@pytest.fixture
def user_gateway(sqlalchemy_session: AsyncSession) -> UserGateway:
    return UserGateway(sqlalchemy_session)


@pytest.fixture
def receipt_gateway(sqlalchemy_session: AsyncSession) -> ReceiptGateway:
    return ReceiptGateway(sqlalchemy_session)
