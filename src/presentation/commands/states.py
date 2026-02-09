from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    get_nickname = State()


class JoinReceiptState(StatesGroup):
    show_receipt = State()
    get_approved = State()


class ProfileState(StatesGroup):
    view = State()
