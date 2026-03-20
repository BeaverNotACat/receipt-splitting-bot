from typing import Protocol, abstractmethod


class OCRRecognizerI(Protocol):
    @abstractmethod
    async def recognize_text(self, image_url: str) -> str:
        raise NotImplementedError
