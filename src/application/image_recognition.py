from typing import Protocol

class ImageRecognitionI(Protocol):

  async def recognize_text(self, image_url: str) -> str:
    pass