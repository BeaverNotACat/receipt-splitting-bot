from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format

from src.presentation.telegram import states

from .common import (
    return_to_profile_button,
    show_bill_button,
    user_prompt_input,
)

chat_window = Window(
    Format("{dialog_data[agent_answer]}"),
    show_bill_button,
    return_to_profile_button,
    user_prompt_input,
    state=states.ReceiptChatSG.chat,
)
