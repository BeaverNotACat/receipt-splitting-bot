from typing import TYPE_CHECKING

from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const, Format

if TYPE_CHECKING:
    from typing import Any

    from aiogram import Bot
    from aiogram_dialog import DialogManager


from src.presentation.telegram import states

from .common import (
    add_dummy_user_button,
    return_to_profile_button,
    show_bill_button,
    user_prompt_input,
)

greetings = Const("""
Привет!
Я - Рожков, ваш персональный помощник в разделении чеков!
Отправьте мне фотогорафии ваших чеков, расскажите текстом\
или голосовым сообщением кто что купил и я посчитаю кому\
сколько нужно заплатить
""")
invite_link = Format("""
Ваша ссылка на приглашение:
{invite_link}
Отправьте её другу, чтобы он присоединился к чеку
""")


async def receipt_dialog_greeting_getter(
    dialog_manager: DialogManager,
    bot: Bot,
    **_: dict[str, Any],
) -> dict[str, Any]:
    receipt_id = states.get_receipt_id(dialog_manager)
    invite_link = await create_start_link(bot, str(receipt_id))
    return {"invite_link": invite_link}


greetings_window = Window(
    greetings,
    invite_link,
    add_dummy_user_button,
    show_bill_button,
    return_to_profile_button,
    user_prompt_input,
    state=states.ReceiptChatSG.greeting,
    getter=receipt_dialog_greeting_getter,
)
