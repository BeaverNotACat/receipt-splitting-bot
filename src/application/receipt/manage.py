import asyncio
from dataclasses import dataclass
from typing import final

from src.application.common import Interactor
from src.application.common.agent import AgentI, AgentResponse, HumanRequest
from src.application.common.asr import RecognizedSpeechText, SpeechRecognizerI
from src.application.common.database import (
    TransactionManagerI,
    UserReaderI,
)
from src.application.common.database.receipt_gateway import ReceiptGatewayI
from src.application.common.ocr import (
    OpticalCharacterRecognizerI,
    RecognizedImageText,
)
from src.application.common.user_provider import UserProviderI
from src.domain.value_objects import (
    AgentMessage,
    Audio,
    MessageText,
    Photo,
    ReceiptID,
)


@dataclass
class ManageReceiptDTO:
    receipt_id: ReceiptID
    text: MessageText | None
    photos: tuple[Photo, ...]
    audios: tuple[Audio, ...]


ManageReceiptResultDTO = AgentMessage


@final
@dataclass(frozen=True)
class ManageReceipt(Interactor[ManageReceiptDTO, ManageReceiptResultDTO]):
    agent: AgentI
    ocr: OpticalCharacterRecognizerI
    asr: SpeechRecognizerI
    user_provider: UserProviderI
    receipt_db_gateway: ReceiptGatewayI
    user_db_gateway: UserReaderI
    transaction_manager: TransactionManagerI

    async def __call__(
        self, context: ManageReceiptDTO
    ) -> ManageReceiptResultDTO:
        response = await self.invoke_agent(context)
        await self.receipt_db_gateway.save_receipt(response.updated_receipt)
        await self.transaction_manager.commit()
        return response.answer

    async def invoke_agent(self, context: ManageReceiptDTO) -> AgentResponse:
        receipt = await self.receipt_db_gateway.fetch_receipt(
            id=context.receipt_id
        )
        participants = await self.user_db_gateway.fetch_users(
            ids=receipt.participants_ids
        )
        request = await self.construct_human_request(context)
        return await self.agent.invoke(request, receipt, participants)

    async def construct_human_request(
        self, context: ManageReceiptDTO
    ) -> HumanRequest:
        current_user = await self.user_provider.fetch_current_user()
        transcribed_audios, transcribed_photos = await self.transcribe_texts(
            context.audios, context.photos
        )
        return HumanRequest(
            current_user.id,
            context.text,
            transcribed_audios,
            transcribed_photos,
        )

    async def transcribe_texts(
        self, audios: tuple[Audio, ...], photos: tuple[Photo, ...]
    ) -> tuple[list[RecognizedSpeechText], list[RecognizedImageText]]:
        audio_future = asyncio.gather(
            *(self.asr.recognize_text(audio) for audio in audios)
        )
        photo_future = asyncio.gather(
            *(self.ocr.recognize_text(photo) for photo in photos)
        )
        return await asyncio.gather(audio_future, photo_future)
