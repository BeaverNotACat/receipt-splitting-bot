from typing import Any

from aiogram.fsm.state import State
from aiogram.types import Message
from aiogram_dialog import Data, Dialog, DialogManager, StartMode, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.text import Const
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.real_user.register import RegisterUser, RegisterUserDTO
from src.domain.value_objects import ChatID, UserNickname

from . import states

NICKNAME_INPUT_ID = "nickname"


@inject
async def on_done(
    message: Message,
    text_input: TextInput,
    dialog_manager: DialogManager,
    nickname: str,
    register_user: FromDishka[RegisterUser],
) -> None:
    dto = RegisterUserDTO(
        ChatID(message.chat.id),
        nickname=UserNickname(nickname),
    )
    await register_user(dto)

    if dialog_manager.dialog_data.get("receipt_id") is not None:
        await dialog_manager.start(states.JoinReceiptState.preview)
    else:
        await dialog_manager.start(states.ProfileState.view)


register_dialog = Dialog(
    Window(
        Const(
            "Введите как вас называют друзья.\n Это необходимо для опознования"
        ),
        TextInput(id=NICKNAME_INPUT_ID, on_success=on_done),
        state=states.RegisterState.nickname,
    ),
)
