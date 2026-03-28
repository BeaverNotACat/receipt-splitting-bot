import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from dishka.integrations.aiogram import setup_dishka

from src.presentation.dependencies import container
from src.presentation.telegram import (
    create_receipt_dialog,
    join_dialog,
    manage_receipt_dialog,
    register_dialog,
    show_profile_dialog,
    start_router,
)
from src.settings import Settings


def get_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start_router)

    dp.include_router(create_receipt_dialog)
    dp.include_router(join_dialog)
    dp.include_router(show_profile_dialog)
    dp.include_router(manage_receipt_dialog)
    dp.include_router(register_dialog)

    setup_dishka(container, dp)
    setup_dialogs(dp)
    return dp


async def run_bot() -> None:
    settings = await container.get(Settings)
    bot = Bot(settings.TELEGRAM_TOKEN.get_secret_value())
    await get_dispatcher().start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
