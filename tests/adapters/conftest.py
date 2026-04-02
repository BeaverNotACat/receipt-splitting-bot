from typing import TYPE_CHECKING

import pytest_asyncio

from src.adapters.database.receipt_gateway import ReceiptGateway
from src.adapters.database.user_gateway import UserGateway
from src.application.common.database.receipt_gateway import ReceiptGatewayI
from src.application.common.database.user_gateway import UserGatewayI

if TYPE_CHECKING:
    from dishka import AsyncContainer


@pytest_asyncio.fixture
async def user_gateway(container: AsyncContainer) -> UserGateway:
    return await container.get(UserGatewayI)


@pytest_asyncio.fixture
async def receipt_gateway(container: AsyncContainer) -> ReceiptGateway:
    return await container.get(ReceiptGatewayI)
