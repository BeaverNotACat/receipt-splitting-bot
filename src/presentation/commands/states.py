from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    nickname = State()


class JoinReceiptState(StatesGroup):
    preview = State()


class ProfileState(StatesGroup):
    view = State()
