from typing import TYPE_CHECKING

import pytest

from src.application.onboard import (
    OnboardUser,
)
from src.domain.services.user import UserService

from .fakes.fake_receipt_gateway import FakeReceiptGateway
from .fakes.fake_user_gateway import FakeUserGateway

if TYPE_CHECKING:
    from src.domain.models.receipt import Receipt


@pytest.fixture
def fake_user_gateway() -> FakeUserGateway:
    return FakeUserGateway()


@pytest.fixture
def fake_receipt_gateway(receipt: Receipt) -> FakeReceiptGateway:
    return FakeReceiptGateway([receipt])


@pytest.fixture
def onboard_user_interactor(
    fake_receipt_gateway: FakeReceiptGateway,
    fake_user_gateway: FakeUserGateway,
) -> OnboardUser:
    return OnboardUser(UserService(), fake_user_gateway, fake_receipt_gateway)
