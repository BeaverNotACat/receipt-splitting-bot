from typing import TYPE_CHECKING

from aiogram.utils.deep_linking import create_start_link

from src.presentation.telegram import states

if TYPE_CHECKING:
    from typing import Any

    from aiogram import Bot
    from aiogram_dialog import DialogManager


async def invite_link_getter(
    dialog_manager: DialogManager,
    bot: Bot,
    **_: dict[str, Any],
) -> dict[str, Any]:
    receipt_id = states.get_receipt_id(dialog_manager)
    invite_link = await create_start_link(bot, str(receipt_id))
    return {"invite_link": invite_link}
