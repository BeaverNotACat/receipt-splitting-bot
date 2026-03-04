from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from src.domain.models import Receipt


@dataclass(slots=True, frozen=True)
class Response:
    answer: str
    receipt: Receipt


class AgentI(Protocol):
    @abstractmethod
    async def invoke(self, user_promp: str, receipt: Receipt) -> Response:
        raise NotImplementedError
