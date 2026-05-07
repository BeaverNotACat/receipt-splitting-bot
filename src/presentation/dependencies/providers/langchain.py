from dishka import Provider, Scope, provide
from langchain_openrouter import ChatOpenRouter

from src.adapters.agent.agent import Agent, AgentModelClient
from src.adapters.asr import ASRModelClient, SpeechRecognizer
from src.adapters.ocr import OCRModelClient, OpticalCharacterRecognizer
from src.application.common.agent import AgentI
from src.application.common.asr import SpeechRecognizerI
from src.application.common.ocr import OpticalCharacterRecognizerI
from src.settings import OpenRouterSettings


class LangChainProvider(Provider):
    scope = Scope.APP

    @provide
    @staticmethod
    def get_ocr_model_client(settings: OpenRouterSettings) -> OCRModelClient:
        return OCRModelClient(
            ChatOpenRouter(  # type: ignore[call-arg]
                model=settings.OCR_MODEL,
                temperature=0,
                api_key=settings.API_KEY,
            )
        )

    @provide
    @staticmethod
    def get_asr_model_client(settings: OpenRouterSettings) -> ASRModelClient:
        return ASRModelClient(
            ChatOpenRouter(  # type: ignore[call-arg]
                model=settings.ASR_MODEL,
                temperature=0,
                api_key=settings.API_KEY,
            )
        )

    @provide
    @staticmethod
    def get_agent_model_client(
        settings: OpenRouterSettings,
    ) -> AgentModelClient:
        return AgentModelClient(
            ChatOpenRouter(  # type: ignore[call-arg]
                model=settings.AGENT_MODEL,
                temperature=0,
                api_key=settings.API_KEY,
                reasoning={"effort": "high", "summary": "auto"},
            )
        )

    orc = provide(
        OpticalCharacterRecognizer, provides=OpticalCharacterRecognizerI
    )
    asr = provide(SpeechRecognizer, provides=SpeechRecognizerI)
    agent = provide(Agent, provides=AgentI)
