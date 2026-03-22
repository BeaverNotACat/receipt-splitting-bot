from copy import deepcopy
from datetime import UTC, datetime
from typing import TYPE_CHECKING
from uuid import uuid7

from src.domain.models.receipt import Receipt, ReceiptItemsData
from src.domain.value_objects import ReceiptID, ReceiptTitle

if TYPE_CHECKING:
    from src.domain.models.user import RealUser


class ReceiptService:
    @staticmethod
    def create_receipt(creditor: RealUser, title: ReceiptTitle) -> Receipt:
        return Receipt(
            id=ReceiptID(uuid7()),
            created_at=datetime.now(tz=UTC),
            title=title,
            creditor_id=creditor.id,
            unassigned_items=[],
            assignees={creditor.id: []},
        )

    @staticmethod
    def narrow_to_items_data(receipt: Receipt) -> ReceiptItemsData:
        """
        Copies Receipt items data
        """
        return ReceiptItemsData(
            receipt.unassigned_items.copy(), deepcopy(receipt.assignees)
        )

    @staticmethod
    def rewrite_receipt_item_data(
        item_data: ReceiptItemsData, receipt: Receipt
    ) -> Receipt:
        """
        Changes receipt unassigned_items and assignes to copies from item_data
        """
        receipt.unassigned_items = item_data.unassigned_items.copy()
        receipt.assignees = deepcopy(item_data.assignees)
        return receipt
