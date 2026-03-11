from typing import TYPE_CHECKING

import pytest
from polyfactory.factories import DataclassFactory
from polyfactory.pytest_plugin import register_fixture

from src.application.receipt.list import ListReceipts, ListReceiptsDTO
from tests.application.fakes.fake_receipt_gateway import FakeReceiptGateway

if TYPE_CHECKING:
    from src.application.common.user_provider import UserProviderI
    from src.domain.models.user import RealUser
    from tests.mocks.domain import ReceiptFactory


@register_fixture
class ListReceiptsDTOFactory(DataclassFactory[ListReceiptsDTO]): ...


RECEIPTS_AS_PARTICIPANT_SIZE = 6
UNRELATED_RECEIPTS_SIZE = 8


@pytest.fixture
def fake_receipt_db_gateway(
    receipt_factory: ReceiptFactory,
    real_user: RealUser,
) -> FakeReceiptGateway:
    debtors_receipts = receipt_factory.batch(
        RECEIPTS_AS_PARTICIPANT_SIZE, assignees={real_user.id: []}
    )
    other_receipts = receipt_factory.batch(UNRELATED_RECEIPTS_SIZE)
    return FakeReceiptGateway([*debtors_receipts, *other_receipts])


@pytest.fixture
def list_receipts_dto(
    list_receipts_dto_factory: ListReceiptsDTOFactory,
) -> ListReceiptsDTO:
    return list_receipts_dto_factory.build()


@pytest.fixture
def list_receipts_interactor(
    fake_receipt_db_gateway: FakeReceiptGateway,
    fake_user_provider: UserProviderI,
) -> ListReceipts:
    return ListReceipts(fake_user_provider, fake_receipt_db_gateway)


async def test_list_receipts(
    list_receipts_dto: ListReceiptsDTO,
    list_receipts_interactor: ListReceipts,
    fake_user_provider: UserProviderI,
) -> None:
    receipts = await list_receipts_interactor(list_receipts_dto)

    creditor = await fake_user_provider.fetch_current_user()
    assert receipts.total == RECEIPTS_AS_PARTICIPANT_SIZE
    for i in receipts.receipts:
        assert creditor.id in i.participants_ids
