from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.models.receipt import Receipt
    from src.domain.value_objects import UserID


def assert_new_receipt_creation(
    receipt: Receipt, creditor_id: UserID, receipt_title: str
) -> None:
    assert receipt.id
    assert receipt.created_at
    assert receipt.title == receipt_title
    assert receipt.creditor_id == creditor_id
    assert receipt.debtors_ids == []
    assert receipt.assignees == {}
