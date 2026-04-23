from aiogram.types import Message
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.input import ManagedTextInput, TextInput
from aiogram_dialog.widgets.kbd import Cancel, Start
from aiogram_dialog.widgets.text import Const
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.receipt.create import CreateReceipt, CreateReceiptDTO
from src.domain.value_objects import ReceiptTitle

from . import states

TITLE_INPUT_ID = "title"


@inject
async def on_done(
    _message: Message,
    _text_input: ManagedTextInput[str],
    dialog_manager: DialogManager,
    title: str,
    create_receipt: FromDishka[CreateReceipt],
) -> None:
    dto = CreateReceiptDTO(receipt_title=ReceiptTitle(title))
    receipt_id = await create_receipt(dto)

    await states.start_receipt_chat(dialog_manager, receipt_id)


create_receipt_dialog = Dialog(
    Window(
        Const("Введите название чека, чтобы после вы смогли его найти"),
        TextInput(id=TITLE_INPUT_ID, on_success=on_done),
        Cancel(Const("↩️ Назад")),
        state=states.CreateReceiptSG.title,
        preview_add_transitions=[
            Start(Const("0"), id="0", state=states.ReceiptChatSG.greeting)
        ],
    ),
)
