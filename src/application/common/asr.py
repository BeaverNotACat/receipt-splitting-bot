from abc import abstractmethod
from typing import BinaryIO, NewType, Protocol

RecognizedSpeechText = NewType("RecognizedSpeechText", str)


class SpeechRecognizerI(Protocol):
    @abstractmethod
    async def recognize_text(self, audio: BinaryIO) -> RecognizedSpeechText:
        raise NotImplementedError
