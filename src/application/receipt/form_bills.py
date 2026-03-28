from dataclasses import dataclass
from typing import final

from src.application.common.database import ReceiptReaderI, UserReaderI
from src.application.common.interactor import Interactor
from src.domain.value_objects import Bill, ReceiptID, UserNickname


@dataclass
class FormBillsDTO:
    receipt_id: ReceiptID


FormBillsResultDTO = list[tuple[UserNickname | None, Bill]]


@final
@dataclass(frozen=True)
class FormBills(Interactor[FormBillsDTO, FormBillsResultDTO]):
    user_db_gateway: UserReaderI
    receipt_db_gateway: ReceiptReaderI

    async def __call__(self, context: FormBillsDTO) -> FormBillsResultDTO:
        receipt = await self.receipt_db_gateway.fetch_receipt(
            id=context.receipt_id
        )
        participants = await self.user_db_gateway.fetch_users(
            ids=receipt.participants_ids
        )
        result: FormBillsResultDTO = []
        for participant in participants:
            result.append(
                (participant.nickname, receipt.form_bill(participant.id))
            )
        result.append((None, receipt.form_bill(None)))

        return result
