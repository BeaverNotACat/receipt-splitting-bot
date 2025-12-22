from typing import TYPE_CHECKING

import pytest
from polyfactory.factories import DataclassFactory
from polyfactory.pytest_plugin import register_fixture

from src.application.onboard import (
    OnboardUser,
    OnboardUserDTO,
)

if TYPE_CHECKING:
    from src.domain.models.receipt import Receipt
    from tests.application.fakes.fake_receipt_gateway import FakeReceiptGateway
    from tests.application.fakes.fake_user_gateway import FakeUserGateway


@register_fixture
class OnboardUserDTOFactory(DataclassFactory[OnboardUserDTO]): ...


@pytest.fixture
def onboard_user_dto(
    onboard_user_dto_factory: OnboardUserDTOFactory, receipt: Receipt
) -> OnboardUserDTO:
    return onboard_user_dto_factory.build(receipt_id=receipt.id)


@pytest.mark.asyncio
async def test_onboard_user(
    onboard_user_dto: OnboardUserDTO,
    onboard_user_interactor: OnboardUser,
    fake_receipt_gateway: FakeReceiptGateway,
    fake_user_gateway: FakeUserGateway,
) -> None:
    await onboard_user_interactor(onboard_user_dto)

    saved_user = next(iter(fake_user_gateway.users_storage.values()))
    saved_receipt = next(iter(fake_receipt_gateway.receipts_storage.values()))
    assert saved_user.name == onboard_user_dto.name
    assert saved_user.id in saved_receipt.debtors_ids
