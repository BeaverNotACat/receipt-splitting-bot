from uuid import UUID

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.fsm.context import FSMContext  # noqa: TC002
from aiogram.types import Message  # noqa: TC002
from dishka.integrations.aiogram import FromDishka, inject

from src.application.real_user.register import RegisterUser, RegisterUserDTO
from src.domain.value_objects import ChatID, UserNickname
from src.presentation.commands.states import (
    JoinReceiptState,
    ProfileState,
    RegisterState,
)

onboard_router = Router()


@onboard_router.message(CommandStart(deep_link=True))
async def deeplink_start(
    message: Message, state: FSMContext, command: CommandObject
) -> None:
    await state.update_data(receipt_id=UUID(command.args))

    if (await state.get_data()).get("user_id") is not None:
        await state.set_state(JoinReceiptState.show_receipt)
        return

    await state.set_state(RegisterState.get_nickname)
    await message.answer(
        "Введите как вас называют друзья",
    )


@onboard_router.message(CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    if (await state.get_data()).get("user_id") is None:
        await state.set_state(RegisterState.get_nickname)
        await message.answer(
            "Введите как вас называют друзья",
        )
    else:
        await state.set_state(ProfileState.view)


@onboard_router.message(RegisterState.get_nickname)
@inject
async def onboard_user(
    message: Message,
    state: FSMContext,
    register_user_interactor: FromDishka[RegisterUser],
) -> None:
    if message.text is None:
        await message.answer(
            "Введите как вас называют друзья",
        )
        return

    dto = RegisterUserDTO(
        chat_id=ChatID(message.chat.id),
        nickname=UserNickname(message.text),
    )
    user_id = await register_user_interactor(dto)

    await state.update_data(user_id=user_id)
    if (await state.get_data()).get("receipt_id") is not None:
        await state.set_state(JoinReceiptState.show_receipt)
    await state.set_state(ProfileState.view)

    await message.answer(
        "ВЫПОЛНЕНО!",
    )
