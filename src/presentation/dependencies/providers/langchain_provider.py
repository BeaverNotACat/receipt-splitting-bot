from dishka import Provider, Scope, provide
from langchain_openrouter import ChatOpenRouter
from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.memory import InMemorySaver

from src.adapters.agent.agent import Agent, AgentModelClient
from src.adapters.ocr import OCRModelClient, OpticalCharacterRecognizer
from src.application.common.agent import AgentI
from src.application.common.ocr import OpticalCharacterRecognizerI
from src.domain.services.receipt import ReceiptService
from src.domain.services.user import UserService
from src.settings import Settings


class LangChainProvider(Provider):
    scope = Scope.APP

    @provide
    @staticmethod
    def get_ocr_model_client(settings: Settings) -> OCRModelClient:
        return OCRModelClient(
            ChatOpenRouter(  # type: ignore[call-arg]
                model="nvidia/nemotron-nano-12b-v2-vl:free",
                temperature=0,
                api_key=settings.OPENROUTER_API_KEY,
            )
        )

    @provide
    @staticmethod
    def get_agent_model_client(settings: Settings) -> AgentModelClient:
        return OCRModelClient(
            ChatOpenRouter(  # type: ignore[call-arg]
                model="nvidia/nemotron-3-super-120b-a12b:free",
                temperature=0,
                api_key=settings.OPENROUTER_API_KEY,
            )
        )

    @provide
    @staticmethod
    def get_checkpointer() -> BaseCheckpointSaver[str]:
        return InMemorySaver()

    @provide
    @staticmethod
    def get_ocr(client: OCRModelClient) -> OpticalCharacterRecognizerI:
        return OpticalCharacterRecognizer(client)

    @provide
    @staticmethod
    def get_agent(
        client: AgentModelClient,
        checkpointer: BaseCheckpointSaver[str],
        user_service: UserService,
        receipt_service: ReceiptService,
    ) -> AgentI:
        return Agent(
            client=client,
            checkpointer=checkpointer,
            user_service=user_service,
            receipt_service=receipt_service,
        )
