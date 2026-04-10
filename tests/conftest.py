from typing import TYPE_CHECKING

import pytest_asyncio
from polyfactory.pytest_plugin import register_fixture

from src.presentation.dependencies import container as app_container
from tests.mocks.domain import (
    DummyUserFactory,
    LineItemFactory,
    RealUserFactory,
    ReceiptFactory,
    dummy_user,
    line_item,
    real_user,
    receipt,
)

if TYPE_CHECKING:
    from collections.abc import AsyncGenerator

    from dishka import AsyncContainer


register_fixture(DummyUserFactory)
register_fixture(LineItemFactory)
register_fixture(RealUserFactory)
register_fixture(ReceiptFactory)


@pytest_asyncio.fixture
async def container() -> AsyncGenerator[AsyncContainer]:
    async with app_container() as request_container:
        yield request_container
    await app_container.close()


__all__ = [
    "dummy_user",
    "line_item",
    "real_user",
    "receipt",
]
