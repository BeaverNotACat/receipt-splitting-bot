from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const

from src.presentation.telegram import states

from .common import (
    add_dummy_user_button,
    invite_link_getter,
    invite_real_user_button,
    return_to_profile_button,
    show_bill_button,
    user_prompt_input,
)

greetings = Const("""
Я - Рожков, ваш персональный помощник в разделении чеков!
Отправьте мне фотографии ваших чеков, расскажите текстом \
или голосовым сообщением, кто что купил, и я посчитаю, \
кому сколько нужно заплатить.\
""")


greetings_window = Window(
    greetings,
    invite_real_user_button,
    add_dummy_user_button,
    show_bill_button,
    return_to_profile_button,
    user_prompt_input,
    state=states.ReceiptChatSG.greeting,
    getter=invite_link_getter,
)
