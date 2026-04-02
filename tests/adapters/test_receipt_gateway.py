from collections.abc import Callable, Coroutine, Iterable
from typing import TYPE_CHECKING, Any

import pytest

from src.domain.models.receipt import Receipt
from src.domain.value_objects import LimitOffsetPagination
from tests.adapters.asserts import assert_receipt

if TYPE_CHECKING:
    from src.adapters.database.receipt_gateway import ReceiptGateway
    from src.adapters.database.user_gateway import UserGateway
    from tests.mocks.domain import RealUserFactory, ReceiptFactory


SetupUsersService = Callable[[Iterable[Receipt]], Coroutine[Any, Any, None]]


@pytest.fixture
def setup_users(
    real_user_factory: RealUserFactory, user_gateway: UserGateway
) -> SetupUsersService:
    async def setup_users_service(receipts: Iterable[Receipt]) -> None:
        user_ids = set()
        for receipt in receipts:
            # TODO(beavernotat): No assignees for creditor
            # https://github.com/BeaverNotACat/receipt-splitting-bot/issues/33
            user_ids.update([*receipt.participants_ids, receipt.creditor_id])

        for obj_id in user_ids:
            await user_gateway.save_user(real_user_factory.build(id=obj_id))
        await user_gateway.session.flush()

    return setup_users_service


RECEIPT_BATCH_SIZE = 10
SetupReceiptsService = Callable[[], Coroutine[Any, Any, list[Receipt]]]


@pytest.fixture
def setup_receipts(
    setup_users: SetupUsersService,
    receipt_factory: ReceiptFactory,
    receipt_gateway: ReceiptGateway,
) -> SetupReceiptsService:
    async def setup_receipts_service() -> list[Receipt]:
        receipts = receipt_factory.batch(RECEIPT_BATCH_SIZE)
        await setup_users(receipts)

        for receipt in receipts:
            await receipt_gateway.save_receipt(receipt)
        await receipt_gateway.session.flush()

        return receipts

    return setup_receipts_service


async def test_receipt_saving(
    receipt: Receipt,
    receipt_gateway: ReceiptGateway,
    setup_users: SetupUsersService,
) -> None:
    await setup_users([receipt])

    await receipt_gateway.save_receipt(receipt)

    assert_receipt(receipt, await receipt_gateway.fetch_receipt(id=receipt.id))


async def test_receipt_updating(
    receipt_factory: ReceiptFactory,
    receipt_gateway: ReceiptGateway,
    setup_users: SetupUsersService,
) -> None:
    initial_receipt = receipt_factory.build()
    updated_receipt = receipt_factory.build(id=initial_receipt.id)
    await setup_users((initial_receipt, updated_receipt))
    await receipt_gateway.save_receipt(initial_receipt)

    await receipt_gateway.save_receipt(updated_receipt)

    assert_receipt(
        updated_receipt,
        await receipt_gateway.fetch_receipt(id=initial_receipt.id),
    )


async def test_receipt_fetching_order(
    receipt_gateway: ReceiptGateway, setup_receipts: SetupReceiptsService
) -> None:
    await setup_receipts()

    selected_receipts = await receipt_gateway.fetch_receipts(
        pagination=LimitOffsetPagination(RECEIPT_BATCH_SIZE, 0)
    )

    for i in range(1, len(selected_receipts)):
        assert selected_receipts[i].id > selected_receipts[i - 1].id


async def test_receipt_counting(
    receipt_gateway: ReceiptGateway, setup_receipts: SetupReceiptsService
) -> None:
    await setup_receipts()

    amount = await receipt_gateway.count_receipts()

    assert amount == RECEIPT_BATCH_SIZE


async def test_receipt_many_filtering(
    receipt_gateway: ReceiptGateway, setup_receipts: SetupReceiptsService
) -> None:
    user_id = (await setup_receipts())[0].creditor_id

    filtered_receipts = await receipt_gateway.fetch_receipts(
        LimitOffsetPagination(RECEIPT_BATCH_SIZE, 0),
        participant_id=user_id,
    )
    receipts_count = await receipt_gateway.count_receipts(
        participant_id=user_id,
    )

    assert receipts_count == len(filtered_receipts)
    for receipt in filtered_receipts:
        assert user_id in receipt.participants_ids
