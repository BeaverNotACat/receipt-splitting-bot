import asyncio

from aiogram import Bot, Dispatcher
from aiogram_dialog import setup_dialogs
from dishka.integrations.aiogram import setup_dishka

from src.presentation.commands.onboard import onboard_router
from src.presentation.dependencies import container
from src.settings import Settings


def get_dispatcher() -> Dispatcher:
    dp = Dispatcher()
    setup_dishka(container, dp)
    setup_dialogs(dp)
    dp.include_router(onboard_router)
    return dp


async def run_bot() -> None:
    settings = await container.get(Settings)
    bot = Bot(settings.TELEGRAM_TOKEN.get_secret_value())
    await get_dispatcher().start_polling(bot)


if __name__ == "__main__":
    asyncio.run(run_bot())
