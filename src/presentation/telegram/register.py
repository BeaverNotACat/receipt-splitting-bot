from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Start
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
    _text_input: ManagedTextInput[str],
    dialog_manager: DialogManager,
    nickname: str,
    register_user: FromDishka[RegisterUser],
) -> None:
    dto = RegisterUserDTO(
        ChatID(message.chat.id),
        nickname=UserNickname(nickname),
    )
    await register_user(dto)

    if isinstance(dialog_manager.start_data, dict):
        await dialog_manager.start(
            states.JoinReceiptSG.preview,
            data={"receipt_id": dialog_manager.start_data["receipt_id"]},
        )
    else:
        await dialog_manager.start(states.ProfileSG.view)


register_dialog = Dialog(
    Window(
        Const(
            "Введите как вас зовут.\n"
            "Мы просим имя, чтобы агент мог отличить вас от"
            "остальных участников чека в текстах сообщений"
        ),
        TextInput(id=NICKNAME_INPUT_ID, on_success=on_done),
        state=states.RegisterSG.nickname,
        preview_add_transitions=[
            Start(Const("0"), id="0", state=states.ProfileSG.view),
        ],
    ),
)
