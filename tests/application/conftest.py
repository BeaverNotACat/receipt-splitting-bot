import pytest

from .fakes.fake_receipt_gateway import FakeReceiptGateway
from .fakes.fake_user_gateway import FakeUserGateway


@pytest.fixture
def fake_user_gateway_factory() -> type[FakeUserGateway]:
    return FakeUserGateway


@pytest.fixture
def fake_receipt_gateway_factory() -> type[FakeReceiptGateway]:
    return FakeReceiptGateway
