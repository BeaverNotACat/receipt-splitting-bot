from typing import TYPE_CHECKING

import pytest
import pytest_asyncio

from src.adapters.database import ReceiptGateway, UserGateway
from src.adapters.user_provider import UserProvider

if TYPE_CHECKING:
    from dishka import AsyncContainer


@pytest.fixture
def user_provider_class() -> type[UserProvider]:
    return UserProvider


@pytest_asyncio.fixture
async def user_gateway(container: AsyncContainer) -> UserGateway:
    return await container.get(UserGateway)


@pytest_asyncio.fixture
async def receipt_gateway(container: AsyncContainer) -> ReceiptGateway:
    return await container.get(ReceiptGateway)
