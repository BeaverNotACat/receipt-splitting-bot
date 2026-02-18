from typing import TYPE_CHECKING

import pytest

from tests.adapters.asserts import assert_receipt

if TYPE_CHECKING:
    from src.adapters.database.receipt_gateway import ReceiptGateway
    from src.adapters.database.user_gateway import UserGateway
    from src.domain.models.receipt import Receipt
    from tests.mocks.domain import RealUserFactory, ReceiptFactory


@pytest.mark.asyncio
async def test_receipt_saving(
    receipt: Receipt,
    real_user_factory: RealUserFactory,
    receipt_gateway: ReceiptGateway,
    user_gateway: UserGateway,
) -> None:
    for user_id in {*receipt.participants_ids, receipt.creditor_id}:
        await user_gateway.save_user(real_user_factory.build(id=user_id))
        await user_gateway.session.flush()

    await receipt_gateway.save_receipt(receipt)

    assert_receipt(receipt, await receipt_gateway.fetch_receipt(id=receipt.id))


@pytest.mark.asyncio
async def test_receipt_updating(
    receipt_factory: ReceiptFactory,
    real_user_factory: RealUserFactory,
    receipt_gateway: ReceiptGateway,
    user_gateway: UserGateway,
) -> None:
    initial_receipt = receipt_factory.build()
    updated_receipt = receipt_factory.build(id=initial_receipt.id)
    for user_id in [
        *initial_receipt.participants_ids,
        *updated_receipt.participants_ids,
        initial_receipt.creditor_id,
        updated_receipt.creditor_id,
    ]:
        await user_gateway.save_user(real_user_factory.build(id=user_id))
        await user_gateway.session.flush()
    await receipt_gateway.save_receipt(initial_receipt)

    await receipt_gateway.save_receipt(updated_receipt)

    assert_receipt(
        updated_receipt,
        await receipt_gateway.fetch_receipt(id=initial_receipt.id),
    )
