from aiogram.types import Message
from aiogram_dialog import DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.text import Const
from dishka.integrations.aiogram_dialog import FromDishka, inject

from src.application.receipt.add_dummy_user import (
    AddDummyUser,
    AddDummyUserDTO,
)
from src.domain.value_objects import UserNickname
from src.presentation.telegram import states
from src.presentation.telegram.manage_receipt.common import get_receipt_id

DUMMY_NICKNAME_INPUT_ID = "dummy_nickname"


@inject
async def on_done(
    _message: Message,
    _text_input: ManagedTextInput[str],
    dialog_manager: DialogManager,
    nickname: str,
    add_dummy_user: FromDishka[AddDummyUser],
) -> None:
    dto = AddDummyUserDTO(
        receipt_id=get_receipt_id(dialog_manager),
        nickname=UserNickname(nickname),
    )
    await add_dummy_user(dto)

    await dialog_manager.back()


add_dummy_window = Window(
    Const("Введите имя участника"),
    TextInput(id=DUMMY_NICKNAME_INPUT_ID, on_success=on_done),
    state=states.ReceiptChatSG.add_dummy,
)
