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

from . import states

start_router = Router()


@start_router.message(CommandStart)
@inject
async def start(
    _message: Message,
    user_provider: FromDishka[UserProviderI],
    dialog_manager: DialogManager,
) -> None:
    try:
        await user_provider.fetch_current_user()
        await dialog_manager.start(
            states.ProfileSG.view, mode=StartMode.RESET_STACK
        )
    except UserIsNotRegisteredError:
        await dialog_manager.start(
            states.RegisterSG.nickname, mode=StartMode.RESET_STACK
        )


@start_router.message(CommandStart(deep_link=True))
@inject
async def deeplink_start(
    _message: Message,
    command: CommandObject,
    user_provider: FromDishka[UserProviderI],
    dialog_manager: DialogManager,
) -> None:
    dialog_manager.dialog_data["receipt_id"] = UUID(command.args)
    try:
        await user_provider.fetch_current_user()
        await dialog_manager.start(
            states.JoinReceiptSG.preview, mode=StartMode.RESET_STACK
        )
    except UserIsNotRegisteredError:
        await dialog_manager.start(
            states.RegisterSG.nickname, mode=StartMode.RESET_STACK
        )
