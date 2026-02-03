from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message  # noqa: TC002
from dishka.integrations.aiogram import FromDishka, inject  # noqa: TC002

from src.application.onboard import OnboardUser, OnboardUserDTO
from src.domain.value_objects import ChatID, UserNickname

onboard_router = Router()


@onboard_router.message(CommandStart)
@inject
async def onboard_user(
    message: Message,
    onboard_user_interactor: FromDishka[OnboardUser],
) -> None:
    dto = OnboardUserDTO(ChatID(message.chat.id), UserNickname("user"))
    await onboard_user_interactor(dto)
    await message.send_copy(chat_id=message.chat.id)
