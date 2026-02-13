from src.application.common.image_decoder import ImageDecoderI
from openai import OpenAI
import requests
import base64

class ImageDecoder(ImageDecoderI):
  def __init__(self, url, base_url, api_key):
    self.url = url
    self.base_url = base_url
    self.api_key = api_key

  def TextRecognition(self):
    client = OpenAI(
        base_url = self.base_url,
        api_key= self.api_key
    )

    response = client.chat.completions.create(
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
                            {"type": "image_url", "image_url": {"url": self.url}
    }
                        ]
                    }
                ]
            )

    text = response.choices[0].message.content
    return text