from typing import Any

from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.text import Const, Format
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.common.user_provider import UserProviderI

from . import states


@inject
async def user_profile_getter(
    user_provider: FromDishka[UserProviderI], **kwargs: dict[str, Any]
) -> dict[str, Any]:
    user = await user_provider.fetch_current_user()
    return {"nickname": user.nickname}


profile_dialog = Dialog(
    Window(
        Format("Добро пожаловать, {nickname}"),
        state=states.ProfileState.view,
        getter=user_profile_getter,
    )
)
