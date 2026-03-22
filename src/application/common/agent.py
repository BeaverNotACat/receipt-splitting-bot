from abc import abstractmethod
from dataclasses import dataclass
from typing import Protocol

from src.domain.models.receipt import Receipt
from src.domain.models.user import User


@dataclass(slots=True, frozen=True)
class AgentResponse:
    answer: str
    receipt: Receipt


class AgentI(Protocol):
    @abstractmethod
    async def invoke(
        self, user_prompt: str, receipt: Receipt, participants: list[User]
    ) -> AgentResponse:
        raise NotImplementedError
