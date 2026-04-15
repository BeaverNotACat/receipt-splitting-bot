from aiogram_dialog import Dialog

from .bills import bills_window
from .chat import chat_window
from .greetings import greetings_window

manage_receipt_dialog = Dialog(greetings_window, chat_window, bills_window)
