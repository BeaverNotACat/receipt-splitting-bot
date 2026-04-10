from abc import abstractmethod
from typing import BinaryIO, NewType, Protocol

RecognizedSpeechText = NewType("RecognizedSpeechText", str)


class SpeechRecognizerI(Protocol):
    """
    Multimodal model wrapper
    Recognizes text in audio and represents it in structured format
    Expectes audio with voice of receipts
    """

    @abstractmethod
    async def recognize_text(self, audio: BinaryIO) -> RecognizedSpeechText:
        raise NotImplementedError