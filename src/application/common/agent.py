from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from src.domain.models import ReceiptItemsData
from src.domain.models.user import User
from src.domain.value_objects import ReceiptID


@dataclass(slots=True, frozen=True)
class Response:
    answer: str
    receipt: ReceiptItemsData


class AgentI(Protocol):
    @abstractmethod
    async def invoke(self, user_prompt: str,
                    receipt_items_data: ReceiptItemsData,
                    users: tuple[User, ...], tread_id: ReceiptID) -> Response:
        raise NotImplementedError
