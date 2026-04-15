from typing import TYPE_CHECKING
from uuid import UUID

from src.domain.value_objects import ReceiptID

if TYPE_CHECKING:
    from aiogram_dialog import DialogManager


def get_receipt_id(dialog_manager: DialogManager) -> ReceiptID:
    return ReceiptID(UUID(dialog_manager.start_data["receipt_id"]))  # type: ignore[call-overload, index]
