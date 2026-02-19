from typing import Any

from aiogram import Bot
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const, Format

from . import states


async def receipt_dialog_greeting_getter(
    dialog_manager: DialogManager,
    bot: Bot,
    **_kwargs: dict[str, Any],
) -> dict[str, Any]:
    receipt_id = dialog_manager.start_data["receipt_id"]  # type: ignore[call-overload, index]
    invite_link = await create_start_link(bot, receipt_id)
    return {"invite_link": invite_link}


receipt_chat_dialog = Dialog(
    Window(
        Format("Ваша ссылка на приглашение:\n{invite_link}"),
        Const("Остальное TBD"),
        Cancel(Const("↩️ Назад")),
        state=states.ReceiptChatSG.greeting,
        getter=receipt_dialog_greeting_getter,
    )
)
