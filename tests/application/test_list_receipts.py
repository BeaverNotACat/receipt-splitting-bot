from typing import TYPE_CHECKING

import pytest

from src.application.list_receipts import ListReceipts
from tests.application.fakes.fake_receipt_gateway import FakeReceiptGateway

if TYPE_CHECKING:
    from src.application.common.user_provider import UserProvider
    from src.domain.models.user import RealUser
    from tests.mocks.domain import ReceiptFactory


@pytest.fixture
def fake_receipt_db_gateway(
    receipt_factory: ReceiptFactory,
    real_user: RealUser,
) -> FakeReceiptGateway:
    creditor_receipts = receipt_factory.batch(2, creditor_id=real_user.id)
    debtors_receipts = receipt_factory.batch(2, debtors_ids=[real_user.id])
    other_receipts = receipt_factory.batch(10)
    return FakeReceiptGateway(
        [*creditor_receipts, *debtors_receipts, *other_receipts]
    )


@pytest.fixture
def list_receipts_interactor(
    fake_receipt_db_gateway: FakeReceiptGateway,
    fake_user_provider: UserProvider,
) -> ListReceipts:
    return ListReceipts(fake_user_provider, fake_receipt_db_gateway)


@pytest.mark.asyncio
async def test_list_receipts(
    list_receipts_interactor: ListReceipts,
    fake_user_provider: UserProvider,
) -> None:
    receipts = await list_receipts_interactor(None)

    creditor = await fake_user_provider.fetch_current_user()
    for i in receipts:
        assert creditor.id in i.participants_ids
