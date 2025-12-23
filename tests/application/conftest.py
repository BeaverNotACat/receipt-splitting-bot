from typing import TYPE_CHECKING

import pytest

from tests.application.fakes.fake_user_provider import FakeUserProvider

from .fakes.fake_receipt_gateway import FakeReceiptGateway
from .fakes.fake_user_gateway import FakeUserGateway

if TYPE_CHECKING:
    from src.application.common.user_provider import UserProvider
    from src.domain.models.user import RealUser


@pytest.fixture
def fake_user_gateway_factory() -> type[FakeUserGateway]:
    return FakeUserGateway


@pytest.fixture
def fake_receipt_gateway_factory() -> type[FakeReceiptGateway]:
    return FakeReceiptGateway


@pytest.fixture
def fake_user_provider(real_user: RealUser) -> UserProvider:
    return FakeUserProvider(real_user)
