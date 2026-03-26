import asyncio
from typing import Any, cast

from aiogram import Bot
from aiogram.types import CallbackQuery, Message, PhotoSize, Voice
from aiogram.utils.deep_linking import create_start_link
from aiogram_dialog import Dialog, DialogManager, ShowMode, Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.text import Const, Format, Jinja
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.receipt.form_bills import FormBills, FormBillsDTO
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
    return {"invite_link": invite_link}


async def on_show_bill(
    _event: CallbackQuery,
    _button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        states.ReceiptChatSG.bills, show_mode=ShowMode.SEND
    )


@inject
async def bills_getter(
    dialog_manager: DialogManager,
    form_bill: FromDishka[FormBills],
    **_kwargs: dict[str, Any],
) -> dict[str, Any]:
    dto = FormBillsDTO(receipt_id=get_receipt_id(dialog_manager))
    bills_mapping = await form_bill(dto)
    await dialog_manager.switch_to(
        states.ReceiptChatSG.chat, show_mode=ShowMode.SEND
    )
    return {"bills": bills_mapping}


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
    await dialog_manager.switch_to(
        states.ReceiptChatSG.chat, show_mode=ShowMode.SEND
    )


return_to_profile_button = Start(
    Const("↩️ К профилю"), id="profile", state=states.ProfileSG.view
)
show_receipt_button = Button(
    Const("📋 Показать чек"), id="show_bill", on_click=on_show_bill
)
user_prompt_input = MessageInput(natural_language_handler)
bills_text = Jinja("""
<b>СЧЕТА:</b>
{% for nickname, bill in bills %}
{% if nickname is none %}
<b>Не назначеные товары:</b>
{% else %}
<b>{{nickname}}:</b>
{% endif %}
Название \t К-во \t Цена \t Сумма
{% for item in bill.items %}
{{item.name}} \t {{item.amount}} \t {{item.price|round(2)}} \t {{item.price*item.amount|round(2)}}
{% endfor %}
Итого: {{bill.total|round(2)}}\n
{% endfor %}
""")  # noqa: E501


manage_receipt_dialog = Dialog(
    Window(
        Const("Рассказ про aгента, что он умеет"),
        Format("Ваша ссылка на приглашение:\n{invite_link}"),
        show_receipt_button,
        return_to_profile_button,
        user_prompt_input,
        state=states.ReceiptChatSG.greeting,
        getter=receipt_dialog_greeting_getter,
    ),
    Window(
        Format("{dialog_data[agent_answer]}"),
        show_receipt_button,
        return_to_profile_button,
        user_prompt_input,
        state=states.ReceiptChatSG.chat,
    ),
    Window(
        bills_text,
        show_receipt_button,
        return_to_profile_button,
        user_prompt_input,
        parse_mode="HTML",
        state=states.ReceiptChatSG.bills,
        getter=bills_getter,
    ),
)
