import base64
import mimetypes
from typing import BinaryIO, NewType, cast

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openrouter import ChatOpenRouter

from src.application.common.ocr import (
    OpticalCharacterRecognizerI,
    RecognizedImageText,
)

OCRModelClient = NewType("OCRModelClient", ChatOpenRouter)


class OpticalCharacterRecognizer(OpticalCharacterRecognizerI):
    def __init__(self, client: OCRModelClient) -> None:
        self.client = client

    async def recognize_text(self, image: BinaryIO) -> RecognizedImageText:
        messages = [
            self._construct_system_message(),
            self._construct_human_message(image),
        ]
        response = await self.client.ainvoke(messages)
        return cast("RecognizedImageText", response.content)

    @staticmethod
    def _construct_system_message() -> SystemMessage:
        return SystemMessage(
            content=(
                "Ты — OCR-модель."
                "Считай только текст c изображения."
                "Выводи строго в одной строке."
                "Сохраняй порядок, как на картинке."
                "Обязательно считай все наименования товаров и цену."
                "Никаких объяснений, комментариев или домыслов."
            )
        )

    @staticmethod
    def _construct_human_message(image: BinaryIO) -> HumanMessage:
        image_type, _ = mimetypes.guess_type(getattr(image, "name", "f.jpg"))
        encoded_image = base64.b64encode(image.read()).decode()
        return HumanMessage(
            content=[
                {"type": "text", "text": "Describe this image."},
                {
                    "type": "image",
                    "base64": encoded_image,
                    "mime_type": image_type,
                },
            ]
        )
