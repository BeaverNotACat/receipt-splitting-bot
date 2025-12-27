from typing import TYPE_CHECKING

import pytest
from polyfactory.factories import DataclassFactory
from polyfactory.pytest_plugin import register_fixture

from src.application.add_dummy_user import AddDummyUser, AddDummyUserDTO
from src.domain.services.user import UserService
from tests.application.fakes.fake_receipt_gateway import FakeReceiptGateway
from tests.application.fakes.fake_user_gateway import FakeUserGateway

if TYPE_CHECKING:
    from tests.application.fakes.fake_user_provider import FakeUserProvider
    from tests.mocks.domain import ReceiptFactory


@register_fixture
class AddDummyUserDTOFactory(DataclassFactory[AddDummyUserDTO]): ...


@pytest.fixture
def add_dummy_user_dto(
    add_dummy_user_dto_factory: AddDummyUserDTOFactory,
) -> AddDummyUserDTO:
    return add_dummy_user_dto_factory.build()


@pytest.fixture
def fake_receipt_db_gateway(
    receipt_factory: ReceiptFactory,
    add_dummy_user_dto: AddDummyUserDTO,
) -> FakeReceiptGateway:
    initial_receipt = receipt_factory.build(id=add_dummy_user_dto.receipt_id)
    return FakeReceiptGateway([initial_receipt])


@pytest.fixture
def fake_user_db_gateway() -> FakeUserGateway:
    return FakeUserGateway()


@pytest.fixture
def add_dummy_user_interactor(
    fake_user_provider: FakeUserProvider,
    fake_receipt_db_gateway: FakeReceiptGateway,
    fake_user_db_gateway: FakeUserGateway,
) -> AddDummyUser:
    return AddDummyUser(
        fake_user_provider,
        UserService(),
        fake_receipt_db_gateway,
        fake_user_db_gateway,
    )


@pytest.mark.asyncio
async def test_add_dummy_user(
    add_dummy_user_dto: AddDummyUserDTO,
    add_dummy_user_interactor: AddDummyUser,
    fake_receipt_db_gateway: FakeReceiptGateway,
) -> None:
    dummy_id = await add_dummy_user_interactor(add_dummy_user_dto)

    saved_receipt = next(
        iter(fake_receipt_db_gateway.receipts_storage.values())
    )
    assert dummy_id in saved_receipt.participants_ids
    assert dummy_id in saved_receipt.assignees
