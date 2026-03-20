import base64
from typing import cast

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openrouter import ChatOpenRouter

from src.application.image_recognition import OCRRecognizerI


class OCRRecognizer(OCRRecognizerI):
    def __init__(self, api_key: str) -> None:
        self.client = ChatOpenRouter(
            model="nvidia/nemotron-nano-12b-v2-vl:free",
            temperature=0,
            api_key=api_key,
        )

    async def recognize_text(self, image_bytes: bytes) -> str:
        b64 = base64.b64encode(image_bytes).decode("utf-8")

        messages = [
            SystemMessage(
                content=(
                    "Ты — OCR-модель."
                    "Считай только текст c изображения."
                    "Выводи строго в одной строке."
                    "Сохраняй порядок, как на картинке."
                    "Обязательно считай все наименования товаров и цену."
                    "Никаких объяснений, комментариев или домыслов."
                )
            ),
            HumanMessage(
                content=[
                    {"type": "text", "text": "Describe this image."},
                    {
                        "type": "image",
                        "url": f"data:image/jpeg;base64,{b64}",
                    },
                ]
            ),
        ]

        response = await self.client.ainvoke(messages)
        return cast("str", response.content).strip()
