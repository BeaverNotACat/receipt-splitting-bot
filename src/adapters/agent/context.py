from typing import TypedDict

from src.domain.models.user import User
from src.domain.value_objects import UserID


class ReceiptModificationContext(TypedDict):
    user_id_mapping: dict[UserID, User]
