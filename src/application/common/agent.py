from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from src.domain.models import ReceiptItemsData
from src.domain.models.receipt import Receipt


@dataclass(slots=True, frozen=True)
class Response:
    answer: str
    receipt: ReceiptItemsData


class AgentI(Protocol):
    @abstractmethod
    async def invoke(
        self,
        receipt: Receipt,
    ) -> Response:
        raise NotImplementedError
