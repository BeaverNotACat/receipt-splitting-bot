from typing import cast

from openai import AsyncOpenAI

from src.application.image_recognition import ImageRecognitionI


class ImageRecognition(ImageRecognitionI):
    def __init__(self, api_endpoint: str, api_key: str) -> None:
        self.client = AsyncOpenAI(
        api_key=api_key,
        base_url=api_endpoint,
        )

    async def recognize_text(self, image_url: str) -> str:
        response = await self.client.chat.completions.create(
            model="nvidia/nemotron-nano-12b-v2-vl:free",
            temperature=0,
            messages=[
            {
                "role": "system",
                "content": [
                    {"type": "text", "text": (
                        "Ты — OCR-модель."
                        "Считай только текст c изображения."
                        "Выводи строго в одной строке."
                        "Сохраняй порядок, как на картинке."
                        "Обязательно считай все наименования товаров и цену."
                        "Никаких объяснений, комментариев или домыслов."
                    )}
                ]
            },
            {
                "role": "user",
                "content": [
                    {"type": "image_url", "image_url": {"url": image_url}}
                ]
            }
        ]
    )

        return cast("str", response.choices[0].message.content)
