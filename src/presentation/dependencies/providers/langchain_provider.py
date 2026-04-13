from typing import BinaryIO

from dishka import Provider, Scope, provide
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver

from src.adapters.agent.agent import Agent, AgentModelClient
from src.adapters.ocr import OCRModelClient, OpticalCharacterRecognizer
from src.application.common.agent import AgentI
from src.application.common.asr import RecognizedSpeechText, SpeechRecognizerI
from src.application.common.ocr import OpticalCharacterRecognizerI
from src.settings import Settings


class LangChainProvider(Provider):
    scope = Scope.APP

    @provide
    @staticmethod
    def get_ocr_model_client(settings: Settings) -> OCRModelClient:
        return OCRModelClient(
            ChatOpenRouter(  # type: ignore[call-arg]
                model=settings.OCR_MODEL,
                temperature=0,
                api_key=settings.OPENROUTER_API_KEY,
            )
        )

    @provide
    @staticmethod
    def get_agent_model_client(settings: Settings) -> AgentModelClient:
        return AgentModelClient(
            ChatOpenRouter(  # type: ignore[call-arg]
                model=settings.AGENT_MODEL,
                temperature=0,
                api_key=settings.OPENROUTER_API_KEY,
            )
        )

    @provide
    @staticmethod
    def get_checkpointer() -> BaseCheckpointSaver[str]:
        return InMemorySaver()

    agent = provide(Agent, provides=AgentI)
    orc = provide(
        OpticalCharacterRecognizer, provides=OpticalCharacterRecognizerI
    )

    @provide
    @staticmethod
    def get_asr() -> SpeechRecognizerI:
        # TODO(beavernotacat): Add speech to text adapter
        # https://github.com/BeaverNotACat/receipt-splitting-bot/issues/38
        class SpeechRecognizer(SpeechRecognizerI):
            async def recognize_text(
                self, audio: BinaryIO
            ) -> RecognizedSpeechText:
                raise NotImplementedError

        return SpeechRecognizer()
