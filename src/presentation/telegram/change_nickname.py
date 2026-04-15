from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.real_user.change_nickname import (
    ChangeNickname,
    ChangeNicknameDTO,
)
from src.domain.value_objects import UserNickname

from . import states

NICKNAME_INPUT_ID = "new_nickname"


@inject
async def on_done(
    _message: Message,
    _text_input: ManagedTextInput[str],
    dialog_manager: DialogManager,
    nickname: str,
    change_nickname: FromDishka[ChangeNickname],
) -> None:
    dto = ChangeNicknameDTO(nickname=UserNickname(nickname))
    await change_nickname(dto)
    await dialog_manager.start(states.ProfileSG.view)


change_nickname_dialog = Dialog(
    Window(
        Const("Введите как вас зовут.\nЭто поможет работе агента"),
        TextInput(id=NICKNAME_INPUT_ID, on_success=on_done),
        Cancel(Const("↩️ Назад")),
        state=states.ChangeNicknameSG.nickname,
    ),
)
