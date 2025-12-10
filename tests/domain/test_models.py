from typing import TYPE_CHECKING

import pytest

from src.domain.exceptions import (
    AlreadyParticipantError,
    RemovedMoreThanExistError,
)

if TYPE_CHECKING:
    from tests.mocks.domain import (
        LineItemFactory,
        RealUserFactory,
        ReceiptFactory,
    )


def test_new_receipt_item_appending(
    receipt_factory: ReceiptFactory, line_item_factory: LineItemFactory
) -> None:
    receipt = receipt_factory.build(unassigned_items=[])
    item = line_item_factory.build()

    receipt.append_item(item)

    assert len(receipt.unassigned_items) == 1
    assert receipt.unassigned_items[0] == item
    assert receipt.unassigned_items[0].amount == item.amount


def test_existing_receipt_item_appending(
    receipt_factory: ReceiptFactory, line_item_factory: LineItemFactory
) -> None:
    item = line_item_factory.build()
    receipt = receipt_factory.build(unassigned_items=[item])

    receipt.append_item(item)

    assert len(receipt.unassigned_items) == 1
    assert receipt.unassigned_items[0] == item
    assert receipt.unassigned_items[0].amount == item.amount * 2


def test_receipt_item_removing(
    receipt_factory: ReceiptFactory, line_item_factory: LineItemFactory
) -> None:
    item = line_item_factory.build()
    receipt = receipt_factory.build(unassigned_items=[item])

    receipt.remove_item(item)

    assert len(receipt.unassigned_items) == 0


def test_more_than_exist_receipt_item_removing(
    receipt_factory: ReceiptFactory, line_item_factory: LineItemFactory
) -> None:
    item = line_item_factory.build()
    item_to_delete = line_item_factory.build(
        name=item.name, amount=item.amount + 1, price=item.price
    )
    receipt = receipt_factory.build(unassigned_items=[item])

    with pytest.raises(RemovedMoreThanExistError):
        receipt.remove_item(item_to_delete)


def test_less_than_exist_receipt_item_removing(
    receipt_factory: ReceiptFactory, line_item_factory: LineItemFactory
) -> None:
    item = line_item_factory.build()
    item_to_delete = line_item_factory.build(
        name=item.name, amount=item.amount / 2, price=item.price
    )
    receipt = receipt_factory.build(unassigned_items=[item])

    receipt.remove_item(item_to_delete)

    assert len(receipt.unassigned_items) == 1
    assert receipt.unassigned_items[0] == item
    assert (
        receipt.unassigned_items[0].amount
        == item.amount - item_to_delete.amount
    )


def test_new_receipt_item_assigning(
    receipt_factory: ReceiptFactory,
    line_item_factory: LineItemFactory,
    real_user_factory: RealUserFactory,
) -> None:
    user = real_user_factory.build()
    item = line_item_factory.build()
    receipt = receipt_factory.build(
        unassigned_items=[item], creditor_id=user.id, assignees={}
    )

    receipt.assign_item(item=item, user=user)

    assert len(receipt.assignees[user.id]) == 1
    assert item == receipt.assignees[user.id][0]
    assert item.amount == receipt.assignees[user.id][0].amount


def test_existing_receipt_item_assigning(
    receipt_factory: ReceiptFactory,
    line_item_factory: LineItemFactory,
    real_user_factory: RealUserFactory,
) -> None:
    user = real_user_factory.build()
    item = line_item_factory.build()
    receipt = receipt_factory.build(
        unassigned_items=[item],
        creditor_id=user.id,
        assignees={user.id: [item]},
    )

    receipt.assign_item(item=item, user=user)

    assert len(receipt.assignees[user.id]) == 1
    assert item == receipt.assignees[user.id][0]
    assert item.amount * 2 == receipt.assignees[user.id][0].amount


def test_line_item_disassigning(
    receipt_factory: ReceiptFactory,
    line_item_factory: LineItemFactory,
    real_user_factory: RealUserFactory,
) -> None:
    item = line_item_factory.build()
    user = real_user_factory.build()
    receipt = receipt_factory.build(
        creditor_id=user.id, assignees={user.id: [item]}
    )

    receipt.disassign_item(item, user)

    assert len(receipt.assignees[user.id]) == 0


def test_more_than_exist_line_item_disassigning(
    receipt_factory: ReceiptFactory,
    line_item_factory: LineItemFactory,
    real_user_factory: RealUserFactory,
) -> None:
    item = line_item_factory.build()
    item_to_delete = line_item_factory.build(
        name=item.name, amount=item.amount + 1, price=item.price
    )
    user = real_user_factory.build()
    receipt = receipt_factory.build(
        creditor_id=user.id, assignees={user.id: [item]}
    )

    with pytest.raises(RemovedMoreThanExistError):
        receipt.disassign_item(item_to_delete, user)


def test_less_than_exist_receipt_item_disassign(
    receipt_factory: ReceiptFactory,
    line_item_factory: LineItemFactory,
    real_user_factory: RealUserFactory,
) -> None:
    item = line_item_factory.build()
    item_to_delete = line_item_factory.build(
        name=item.name, amount=item.amount / 2, price=item.price
    )
    user = real_user_factory.build()
    receipt = receipt_factory.build(
        creditor_id=user.id, assignees={user.id: [item]}
    )

    receipt.disassign_item(item_to_delete, user)

    assert len(receipt.assignees[user.id]) == 1
    assert receipt.assignees[user.id][0] == item
    assert (
        receipt.assignees[user.id][0].amount
        == item.amount - item_to_delete.amount
    )


def test_user_appending(
    receipt_factory: ReceiptFactory,
    real_user_factory: RealUserFactory,
) -> None:
    user = real_user_factory.build()
    receipt = receipt_factory.build(debtors_ids=[])

    receipt.append_debtor(user)

    assert len(receipt.debtors_ids) == 1
    assert receipt.assignees[user.id] == []


def test_participant_user_appending(
    receipt_factory: ReceiptFactory,
    real_user_factory: RealUserFactory,
) -> None:
    user = real_user_factory.build()
    receipt = receipt_factory.build(creditor_id=user.id)

    with pytest.raises(AlreadyParticipantError):
        receipt.append_debtor(user)


def test_user_removing(
    receipt_factory: ReceiptFactory,
    real_user_factory: RealUserFactory,
) -> None:
    user = real_user_factory.build()
    receipt = receipt_factory.build(
        debtors_ids=[user.id], assignees={user.id: []}
    )

    receipt.remove_debtor(user)

    assert len(receipt.debtors_ids) == 0
    assert receipt.assignees.get(user.id, None) is None
