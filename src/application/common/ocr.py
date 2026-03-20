from abc import abstractmethod
from typing import BinaryIO, NewType, Protocol


RecognizedImageText = NewType("RecognizedImageText", str)


class OpticalCharacterRecognizerI(Protocol):
    """
    Multimodal model wrapper
    Recognizes text and represents it in structured format
    Expectes to obtains photos of receipts
    """

    @abstractmethod
    async def recognize_text(self, image: BinaryIO) -> ReceiptText:
        raise NotImplementedError
