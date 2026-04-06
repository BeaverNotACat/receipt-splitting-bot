import asyncio
from typing import TYPE_CHECKING

from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from dishka.integrations.aiogram_dialog import FromDishka, inject

from src.application.receipt.manage import ManageReceipt, ManageReceiptDTO
from src.domain.value_objects import Audio, MessageText, Photo
from src.presentation.telegram import states

from .get_receipt_id import get_receipt_id

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import Message, PhotoSize, Voice


async def download_photos(
    bot: Bot, photo_sizes: list[PhotoSize] | None
) -> tuple[Photo, ...]:
    if photo_sizes is None:
        return ()

    # PhotoSize array has duplicates with different resolution
    file_ids = {photo.file_id for photo in photo_sizes}
    tasks = (bot.download(file_id) for file_id in file_ids)

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
    await dialog_manager.switch_to(
        states.ReceiptChatSG.chat, show_mode=ShowMode.SEND
    )


user_prompt_input = MessageInput(natural_language_handler)
