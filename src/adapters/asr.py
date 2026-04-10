import base64
import mimetypes
from typing import BinaryIO, NewType, cast

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_openrouter import ChatOpenRouter

from src.application.common.asr import (
    SpeechRecognizerI,
    RecognizedSpeechText,
)

ASRModelClient = NewType("ASRModelClient", ChatOpenRouter)


class SpeechRecognizer(SpeechRecognizerI):
    def __init__(self, client: ASRModelClient) -> None:
        self.client = client

    async def recognize_text(self, audio: BinaryIO) -> RecognizedSpeechText:
        messages = [
            self._construct_system_message(),
            self._construct_human_message(audio),
        ]
        response = await self.client.ainvoke(messages)
        return cast("RecognizedSpeechText", response.content)

    @staticmethod
    def _construct_system_message() -> SystemMessage:
        return SystemMessage(
            content=(
                "Ты — ASR-модель. "
                "Распознай речь из аудио."
                "Выводи строго в одной строке."
                "Без комментариев и объяснений."
            )
        )

    @staticmethod
    def _construct_human_message(audio: BinaryIO) -> HumanMessage:
        audio_type, _ = mimetypes.guess_type(audio.name)
        encoded_audio = base64.b64encode(audio.read()).decode()

        return HumanMessage(
            content=[
                {"type": "text", "text": "Transcribe this audio."},
                {
                    "type": "input_audio",
                    "input_audio": {
                        "data": encoded_audio,
                        "format": audio_type.split("/")[-1] if audio_type else "ogg",
                    },
                },
            ]
        )