from typing import TYPE_CHECKING

from aiogram_dialog import ShowMode
from aiogram_dialog.widgets.kbd import Button, Start
from aiogram_dialog.widgets.text import Const

from src.presentation.telegram import states

if TYPE_CHECKING:
    from aiogram.types import CallbackQuery
    from aiogram_dialog import DialogManager


async def on_show_bill(
    _event: CallbackQuery,
    _button: Button,
    dialog_manager: DialogManager,
) -> None:
    await dialog_manager.switch_to(
        states.ReceiptChatSG.bills, show_mode=ShowMode.SEND
    )


async def on_add_dummy_user(
    _event: CallbackQuery,
    _button: Button,
    dialog_manager: DialogManager,
) -> None:
    await states.start_add_dummy_user(
        dialog_manager, states.get_receipt_id(dialog_manager)
    )


return_to_profile_button = Start(
    Const("↩️ К профилю"), id="profile", state=states.ProfileSG.view
)
show_bill_button = Button(
    Const("📋 Показать чек"), id="show_bill", on_click=on_show_bill
)
add_dummy_user_button = Button(
    Const("👥 Добавить виртуального участника"),
    id="add_dummy_user",
    on_click=on_add_dummy_user,
)

# preview_add_transitions = [
#     Start(Const("0"), id="0", state=states.ReceiptChatSG.)
# ]
