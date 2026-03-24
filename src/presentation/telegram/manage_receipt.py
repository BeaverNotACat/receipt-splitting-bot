import asyncio
from typing import Any, cast

from aiogram import Bot
from aiogram.types import Message, PhotoSize, Voice
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const, Format
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.receipt.manage import ManageReceipt, ManageReceiptDTO
from src.domain.value_objects import Audio, MessageText, Photo, ReceiptID

from . import states


def get_receipt_id(dialog_manager: DialogManager) -> ReceiptID:
    return cast(ReceiptID, dialog_manager.start_data["receipt_id"])  # type: ignore[call-overload, index]


async def receipt_dialog_greeting_getter(
    dialog_manager: DialogManager,
    bot: Bot,
    **_: dict[str, Any],
) -> dict[str, Any]:
    receipt_id = get_receipt_id(dialog_manager)
    invite_link = await create_start_link(bot, str(receipt_id))
    await dialog_manager.next()
    return {"invite_link": invite_link}


async def download_photos(
    bot: Bot, photos: list[PhotoSize] | None
) -> tuple[Photo, ...]:
    if photos is None:
        return ()
    tasks = [bot.download(photo.file_id) for photo in photos]
    return tuple(
        Photo(photo)
        for photo in (await asyncio.gather(*tasks))
        if photo is not None
    )


async def download_audios(bot: Bot, voice: Voice | None) -> tuple[Audio, ...]:
    if voice is None:
        return ()
    audio = await bot.download(voice.file_id)
    if audio is None:
        return ()
    return (Audio(audio),)


@inject
async def natural_language_handler(
    message: Message,
    _message_input: MessageInput,
    dialog_manager: DialogManager,
    manage_receipt: FromDishka[ManageReceipt],
) -> None:
    if message.bot is None:
        raise ValueError

    dto = ManageReceiptDTO(
        receipt_id=get_receipt_id(dialog_manager),
        text=MessageText(message.text) if message.text is not None else None,
        photos=await download_photos(message.bot, message.photo),
        audios=await download_audios(message.bot, message.voice),
    )
    answer = await manage_receipt(dto)
    dialog_manager.dialog_data["agent_answer"] = answer


manage_receipt_dialog = Dialog(
    Window(
        Const("{Рассказ про гента, что он умеет}"),
        Format("Ваша ссылка на приглашение:\n{invite_link}"),
        Start(Const("↩️ К профилю"), id="profile", state=states.ProfileSG.view),
        MessageInput(natural_language_handler),
        state=states.ReceiptChatSG.greeting,
        getter=receipt_dialog_greeting_getter,
    ),
    Window(
        Format("{dialog_data[agent_answer]}"),
        Start(Const("↩️ К профилю"), id="profile", state=states.ProfileSG.view),
        MessageInput(natural_language_handler),
        state=states.ReceiptChatSG.chat,
    ),
)
