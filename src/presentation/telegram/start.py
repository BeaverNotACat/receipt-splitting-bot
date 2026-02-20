from uuid import UUID

from aiogram import Router
from aiogram.filters import CommandObject, CommandStart
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode
from dishka.integrations.aiogram import FromDishka, inject

from src.application.common.user_provider import (
    UserIsNotRegisteredError,
    UserProviderI,
)
from src.domain.value_objects import ReceiptID

from . import states

start_router = Router()


@start_router.message(CommandStart(deep_link=True))
@inject
async def deeplink_start(
    _message: Message,
    command: CommandObject,
    user_provider: FromDishka[UserProviderI],
    dialog_manager: DialogManager,
) -> None:
    try:
        initial_state = states.JoinReceiptSG.preview
        await user_provider.fetch_current_user()
    except UserIsNotRegisteredError:
        initial_state = states.RegisterSG.nickname

    await dialog_manager.start(
        initial_state,
        mode=StartMode.RESET_STACK,
        data={"receipt_id": ReceiptID(UUID(command.args))},
    )


@start_router.message(CommandStart())
@inject
async def start(
    _message: Message,
    user_provider: FromDishka[UserProviderI],
    dialog_manager: DialogManager,
) -> None:
    try:
        initial_state = states.ProfileSG.view
        await user_provider.fetch_current_user()
    except UserIsNotRegisteredError:
        initial_state = states.RegisterSG.nickname

    await dialog_manager.start(initial_state, mode=StartMode.RESET_STACK)
