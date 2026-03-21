from collections.abc import Iterable
from typing import TYPE_CHECKING

from src.domain.value_objects import LimitOffsetPagination, UserID
from tests.adapters.asserts import assert_receipt

if TYPE_CHECKING:
    from src.adapters.database.receipt_gateway import ReceiptGateway
    from src.adapters.database.user_gateway import UserGateway
    from src.domain.models.receipt import Receipt
    from tests.mocks.domain import RealUserFactory, ReceiptFactory


async def setup_users(
    ids: Iterable[UserID], *, factory: RealUserFactory, gateway: UserGateway
) -> None:
    for obj_id in ids:
        await gateway.save_user(factory.build(id=obj_id))
    await gateway.session.flush()


async def test_receipt_saving(
    receipt: Receipt,
    real_user_factory: RealUserFactory,
    receipt_gateway: ReceiptGateway,
    user_gateway: UserGateway,
) -> None:
    await setup_users(
        receipt.participants_ids,
        factory=real_user_factory,
        gateway=user_gateway,
    )

    await receipt_gateway.save_receipt(receipt)

    assert_receipt(receipt, await receipt_gateway.fetch_receipt(id=receipt.id))


async def test_receipt_updating(
    receipt_factory: ReceiptFactory,
    real_user_factory: RealUserFactory,
    receipt_gateway: ReceiptGateway,
    user_gateway: UserGateway,
) -> None:
    initial_receipt = receipt_factory.build()
    updated_receipt = receipt_factory.build(id=initial_receipt.id)
    await setup_users(
        {
            *initial_receipt.participants_ids,
            *updated_receipt.participants_ids,
            # TODO(beavernotat): No assignees for creditor
            # https://github.com/BeaverNotACat/receipt-splitting-bot/issues/33
            initial_receipt.creditor_id,
            updated_receipt.creditor_id,
        },
        factory=real_user_factory,
        gateway=user_gateway,
    )
    await receipt_gateway.save_receipt(initial_receipt)

    await receipt_gateway.save_receipt(updated_receipt)

    assert_receipt(
        updated_receipt,
        await receipt_gateway.fetch_receipt(id=initial_receipt.id),
    )


RECEIPT_BATCH_SIZE = 10


async def test_receipt_fetching_order(
    receipt_factory: ReceiptFactory,
    real_user_factory: RealUserFactory,
    receipt_gateway: ReceiptGateway,
    user_gateway: UserGateway,
) -> None:
    receipts = receipt_factory.batch(RECEIPT_BATCH_SIZE)
    user_ids = set()
    for receipt in receipts:
        user_ids.update([*receipt.participants_ids, receipt.creditor_id])
    await setup_users(
        user_ids,
        factory=real_user_factory,
        gateway=user_gateway,
    )
    for receipt in receipts:
        await receipt_gateway.save_receipt(receipt)
    await receipt_gateway.session.flush()

    selected_receipts = await receipt_gateway.fetch_receipts(
        pagination=LimitOffsetPagination(RECEIPT_BATCH_SIZE, 0)
    )
    for i in range(1, len(selected_receipts)):
        assert selected_receipts[i].id > selected_receipts[i - 1].id
