from src.application.common.image_decoder import ImageRecognitionI
from openai import AsyncOpenAI
import asyncio

class ImageRecognition(ImageRecognitionI):
  def __init__(self, api_endpoint: str, api_key: str):
    self.client = AsyncOpenAI(
      api_key= api_key,
      base_url = api_endpoint,
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
                      "Ты — OCR-модель. Считай только текст с изображения. "
                      "Выводи строго в одной строке, в том же порядке, как на картинке. "
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

    text = response.choices[0].message.content
    return text