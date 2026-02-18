from aiogram_dialog import Dialog, Window
from aiogram_dialog.widgets.kbd import Cancel
from aiogram_dialog.widgets.text import Const

from . import states

receipt_chat_dialog = Dialog(
    Window(
        Const("TBD"),
        Cancel(Const("↩️ Назад")),
        state=states.ReceiptChatSG.greeting,
    )
)
