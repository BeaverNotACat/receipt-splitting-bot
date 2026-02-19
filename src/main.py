import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from dishka.integrations.aiogram import setup_dishka

from src.presentation.commands.create_receipt import create_receipt_dialog
from src.presentation.commands.join_receipt import join_dialog
from src.presentation.commands.profile import profile_dialog
from src.presentation.commands.receipt_chat import receipt_chat_dialog
from src.presentation.commands.register import register_dialog
from src.presentation.commands.start import start_router
from src.presentation.dependencies import container
from src.settings import Settings


def get_dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(start_router)
    dp.include_router(profile_dialog)
    dp.include_router(register_dialog)
    dp.include_router(create_receipt_dialog)
    dp.include_router(join_dialog)
    dp.include_router(receipt_chat_dialog)
    setup_dishka(container, dp)
    setup_dialogs(dp)
    return dp


async def run_bot() -> None:
    settings = await container.get(Settings)
    bot = Bot(settings.TELEGRAM_TOKEN.get_secret_value())
    await get_dispatcher().start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
