import pytest

from src.adapters.database.receipt_gateway import ReceiptGateway
from src.adapters.database.user_gateway import UserGateway
from src.domain.models.receipt import Receipt
from src.domain.value_objects import UserID
from tests.mocks.domain import RealUserFactory


async def set_up_users(
    users_ids: list[UserID],
    user_gateway: UserGateway,
    real_user_factory: RealUserFactory,
) -> None:
    for user_id in users_ids:
        await user_gateway.save_user(real_user_factory.build(id=user_id))


@pytest.mark.asyncio
async def test_receipt_saving(
    receipt: Receipt,
    real_user_factory: RealUserFactory,
    receipt_gateway: ReceiptGateway,
    user_gateway: UserGateway,
) -> None:
    for user_id in [*receipt.participants_ids, receipt.creditor_id]:
        await user_gateway.save_user(real_user_factory.build(id=user_id))
        await user_gateway.session.flush()

    await receipt_gateway.save_receipt(receipt)

    saved_receipt = await receipt_gateway.fetch_receipt()
    assert saved_receipt.id == receipt.id
    assert saved_receipt.created_at == receipt.created_at
    assert saved_receipt.title == receipt.title
    assert saved_receipt.creditor_id == receipt.creditor_id
    assert len(saved_receipt.unassigned_items) == len(receipt.unassigned_items)
    for item in saved_receipt.unassigned_items:
        assert item in receipt.unassigned_items
    assert len(saved_receipt.assignees) == len(saved_receipt.assignees)
    for user_id in receipt.assignees:
        for item in receipt.assignees[user_id]:
            assert item in saved_receipt.assignees[user_id]
