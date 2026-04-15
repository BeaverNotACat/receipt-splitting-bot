from typing import TYPE_CHECKING

from aiogram.types import Message
from aiogram_dialog import DialogManager, ShowMode
from aiogram_dialog.widgets.input import MessageInput
from dishka.integrations.aiogram_dialog import FromDishka, inject

from src.application.receipt.manage import ManageReceipt, ManageReceiptDTO
from src.domain.value_objects import Audio, MessageText, Photo
from src.presentation.telegram import states

if TYPE_CHECKING:
    from aiogram import Bot
    from aiogram.types import Message, PhotoSize, Voice


async def download_photos(
    bot: Bot, photo_sizes: list[PhotoSize] | None
) -> tuple[Photo, ...]:
    if photo_sizes is None:
        return ()

    # Each attached photo is actually separate message
    # With 4 PhotoSizes from lowest to highest
    photo = await bot.download(photo_sizes[-1])
    if photo is None:
        return ()

    return (Photo(photo),)


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
        receipt_id=states.get_receipt_id(dialog_manager),
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
