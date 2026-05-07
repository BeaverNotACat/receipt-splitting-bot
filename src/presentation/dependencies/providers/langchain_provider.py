from dishka import Provider, Scope, provide
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver

from src.adapters.agent.agent import Agent, AgentModelClient
from src.adapters.asr import ASRModelClient, SpeechRecognizer
from src.adapters.ocr import OCRModelClient, OpticalCharacterRecognizer
from src.application.common.agent import AgentI
from src.application.common.asr import SpeechRecognizerI
from src.application.common.ocr import OpticalCharacterRecognizerI
from src.settings import Settings


class LangChainProvider(Provider):
    scope = Scope.APP

    @provide
    @staticmethod
    def get_checkpointer() -> BaseCheckpointSaver[str]:
        return InMemorySaver()

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
    def get_asr_model_client(settings: Settings) -> ASRModelClient:
        return ASRModelClient(
            ChatOpenRouter(  # type: ignore[call-arg]
                model=settings.ASR_MODEL,
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
                reasoning={"effort": "high", "summary": "auto"},
            )
        )

    orc = provide(
        OpticalCharacterRecognizer, provides=OpticalCharacterRecognizerI
    )
    asr = provide(SpeechRecognizer, provides=SpeechRecognizerI)
    agent = provide(Agent, provides=AgentI)
