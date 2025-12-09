from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid7

from src.domain.models.receipt import Receipt
from src.domain.value_objects import ReceiptID

if TYPE_CHECKING:
    from src.domain.models.user import RealUser


def create_receipt(creditor: RealUser, title: str) -> Receipt:
    return Receipt(
        id=ReceiptID(uuid7()),
        created_at=datetime.now(tz=UTC),
        title=title,
        creditor_id=creditor.id,
        debtors_ids=[],
        unassigned_items=[],
        assignees={},
    )
