from abc import abstractmethod
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Protocol

from src.application.common.asr import RecognizedSpeechText
from src.application.common.ocr import RecognizedImageText
from src.domain.models.receipt import Receipt
from src.domain.models.user import User
from src.domain.value_objects import AgentMessage, MessageText


@dataclass(slots=True, frozen=True)
class HumanRequest:
    users_input: MessageText | None
    transcribed_audios: Sequence[RecognizedSpeechText]
    transcribed_photos: Sequence[RecognizedImageText]


@dataclass(slots=True, frozen=True)
class AgentResponse:
    answer: AgentMessage
    updated_receipt: Receipt


class AgentI(Protocol):
    @abstractmethod
    async def invoke(
        self, request: HumanRequest, receipt: Receipt, participants: list[User]
    ) -> AgentResponse:
        raise NotImplementedError
