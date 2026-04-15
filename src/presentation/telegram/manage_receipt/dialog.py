from aiogram_dialog import Dialog

from .add_dummy import add_dummy_window
from .bills import bills_window
from .chat import chat_window
from .greetings import greetings_window

manage_receipt_dialog = Dialog(
    greetings_window, add_dummy_window, chat_window, bills_window
)
