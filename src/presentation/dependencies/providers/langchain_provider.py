from dishka import Provider, Scope, provide
from langchain_openrouter import ChatOpenRouter

from src.adapters.ocr import OCRModelClient, OpticalCharacterRecognizer
from src.application.common.ocr import OpticalCharacterRecognizerI
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
    def get_ocr(client: OCRModelClient) -> OpticalCharacterRecognizerI:
        return OpticalCharacterRecognizer(client)
