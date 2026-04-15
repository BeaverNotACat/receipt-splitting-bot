from uuid import UUID

from aiogram.fsm.state import State, StatesGroup
from aiogram_dialog import DialogManager, ShowMode

from src.domain.value_objects import ReceiptID


class RegisterSG(StatesGroup):
    nickname = State()


class ChangeNicknameSG(StatesGroup):
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


class AddDummyUserSG(StatesGroup):
    nickname = State()


async def start_receipt_chat(
    dialog_manager: DialogManager, receipt_id: ReceiptID
) -> None:
    await dialog_manager.start(
        ReceiptChatSG.greeting, data={"receipt_id": str(receipt_id)}
    )


async def start_add_dummy_user(
    dialog_manager: DialogManager, receipt_id: ReceiptID
) -> None:
    await dialog_manager.start(
        AddDummyUserSG.nickname,
        data={"receipt_id": str(receipt_id)},
        show_mode=ShowMode.SEND,
    )


def get_receipt_id(dialog_manager: DialogManager) -> ReceiptID:
    return ReceiptID(UUID(dialog_manager.start_data["receipt_id"]))  # type: ignore[call-overload, index]
