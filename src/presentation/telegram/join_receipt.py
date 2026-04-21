from typing import Any, cast

from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.text import Const, Format
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.receipt.get import GetReceipt, GetReceiptDTO
from src.application.receipt.join import JoinReceipt, JoinReceiptDTO
from src.domain.value_objects import ReceiptID

from . import states


def obtain_receipt_id(dialog_manager: DialogManager) -> ReceiptID:
    return cast(
        ReceiptID,
        dialog_manager.start_data["receipt_id"],  # type: ignore[call-overload, index]
    )


@inject
async def user_profile_getter(
    dialog_manager: DialogManager,
    get_receipt: FromDishka[GetReceipt],
    **_kwargs: dict[str, Any],
) -> dict[str, Any]:
    receipt_id: ReceiptID = obtain_receipt_id(dialog_manager)
    dto = GetReceiptDTO(receipt_id=receipt_id)

    receipt = await get_receipt(dto)

    return {
        "title": receipt.title,
        "nickname": receipt.creditor_id,
    }


@inject
async def on_approve(
    _event: CallbackQuery,
    _button: Button,
    dialog_manager: DialogManager,
    join_receipt: FromDishka[JoinReceipt],
) -> None:
    receipt_id: ReceiptID = obtain_receipt_id(dialog_manager)
    dto = JoinReceiptDTO(receipt_id=receipt_id)

    await join_receipt(dto)

    await states.start_receipt_chat(dialog_manager, receipt_id)


join_dialog = Dialog(
    Window(
        Format("Вы собираетесь присоединиться к чеку c названием {title}\n"),
        Button(Const("✅"), id="approve", on_click=on_approve),
        Start(Const("❌"), id="cancel", state=states.ProfileSG.view),
        state=states.JoinReceiptSG.preview,
        getter=user_profile_getter,
        preview_add_transitions=[
            Start(Const("0"), id="0", state=states.ReceiptChatSG.greeting),
        ],
    )
)
