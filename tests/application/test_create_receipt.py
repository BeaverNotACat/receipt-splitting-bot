from typing import TYPE_CHECKING

import pytest
from polyfactory.factories import DataclassFactory
from polyfactory.pytest_plugin import register_fixture

from src.application.create_receipt import CreateReceipt, CreateReceiptDTO
from src.domain.services.receipt import ReceiptService

if TYPE_CHECKING:
    from src.application.common.user_provider import UserProvider
    from tests.application.fakes.fake_receipt_gateway import FakeReceiptGateway


@register_fixture
class CreateReceiptDTOFactory(DataclassFactory[CreateReceiptDTO]): ...


@pytest.fixture
def fake_receipt_gateway(
    fake_receipt_gateway_factory: type[FakeReceiptGateway],
) -> FakeReceiptGateway:
    return fake_receipt_gateway_factory()


@pytest.fixture
def create_receipt_interactor(
    fake_receipt_gateway: FakeReceiptGateway,
    fake_user_provider: UserProvider,
) -> CreateReceipt:
    return CreateReceipt(
        ReceiptService(), fake_receipt_gateway, fake_user_provider
    )


@pytest.mark.asyncio
async def test_create_receipt(
    create_receipt_dto_factory: CreateReceiptDTOFactory,
    create_receipt_interactor: CreateReceipt,
    fake_receipt_gateway: FakeReceiptGateway,
    fake_user_provider: UserProvider,
) -> None:
    context = create_receipt_dto_factory.build()

    await create_receipt_interactor(context)

    saved_receipt = next(iter(fake_receipt_gateway.receipts_storage.values()))
    creditor = await fake_user_provider.fetch_current_user()
    assert saved_receipt.title == context.receipt_title
    assert saved_receipt.creditor_id == creditor.id
