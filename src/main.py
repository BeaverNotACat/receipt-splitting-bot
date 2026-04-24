import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram_dialog import setup_dialogs
from dishka.integrations.aiogram import setup_dishka
from langchain_core.globals import set_debug
from redis.asyncio import Redis

from src.presentation.dependencies import container
from src.presentation.telegram import (
    add_dummy_user_dialog,
    change_nickname_dialog,
    create_receipt_dialog,
    join_dialog,
    manage_receipt_dialog,
    register_dialog,
    show_profile_dialog,
    start_router,
)
from src.settings import Settings


def setup_langchain_globals(settings: Settings) -> None:
    set_debug(settings.DEBUG)


def get_dispatcher(storage_client: Redis) -> Dispatcher:
    storage = RedisStorage(
        storage_client, DefaultKeyBuilder(with_destiny=True)
    )

    dp = Dispatcher(storage=storage)

    dp.include_router(start_router)

    dp.include_router(add_dummy_user_dialog)
    dp.include_router(change_nickname_dialog)
    dp.include_router(create_receipt_dialog)
    dp.include_router(join_dialog)
    dp.include_router(show_profile_dialog)
    dp.include_router(manage_receipt_dialog)
    dp.include_router(register_dialog)

    setup_dishka(container, dp)
    setup_dialogs(dp)
    return dp


async def run_bot(settings: Settings) -> None:
    setup_langchain_globals(settings)

    bot = Bot(settings.TELEGRAM_TOKEN.get_secret_value())

    redis_client = await container.get(Redis)
    await get_dispatcher(redis_client).start_polling(bot)


if __name__ == "__main__":
    settings = container.get_sync(Settings)
    asyncio.run(run_bot(settings), debug=settings.DEBUG)
