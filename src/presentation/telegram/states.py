from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import DialogManager

from src.domain.value_objects import ReceiptID


class RegisterSG(StatesGroup):
    nickname = State()


class JoinReceiptSG(StatesGroup):
    preview = State()


class ProfileSG(StatesGroup):
    view = State()


class CreateReceiptSG(StatesGroup):
    title = State()


class ReceiptChatSG(StatesGroup):
    greeting = State()
    bills = State()
    chat = State()


async def start_receipt_chat(
    dialog_manager: DialogManager, receipt_id: ReceiptID
) -> None:
    await dialog_manager.start(
        ReceiptChatSG.greeting, data={"receipt_id": receipt_id}
    )
