from aiogram.fsm.state import State, StatesGroup


class RegisterSG(StatesGroup):
    nickname = State()


class JoinReceiptSG(StatesGroup):
    preview = State()


class ProfileSG(StatesGroup):
    view = State()


class CreateReceiptSG(StatesGroup):
    title = State()


class ReceiptChatSG(StatesGroup):
    greeting = State()
    chat = State()
