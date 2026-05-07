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
from src.settings import GlobalSettings
from src.settings.telegram import TelegramSettings

aiogram_routes = (
    start_router,
    add_dummy_user_dialog,
    change_nickname_dialog,
    create_receipt_dialog,
    join_dialog,
    show_profile_dialog,
    manage_receipt_dialog,
    register_dialog,
)


def get_dispatcher(storage_client: Redis) -> Dispatcher:
    storage = RedisStorage(
        storage_client, DefaultKeyBuilder(with_destiny=True)
    )

    dp = Dispatcher(storage=storage)
    dp.include_routers(*aiogram_routes)

    setup_dishka(container, dp)
    setup_dialogs(dp)
    return dp


async def run_bot(token: str, redis: Redis) -> None:
    bot = Bot(token)
    await get_dispatcher(redis).start_polling(bot)


def main() -> None:
    settings = container.get_sync(GlobalSettings)
    telegram_settings = container.get_sync(TelegramSettings)
    redis = container.get_sync(Redis)

    set_debug(settings.DEBUG)

    asyncio.run(
        run_bot(
            token=telegram_settings.TOKEN.get_secret_value(),
            redis=redis,
        ),
        debug=settings.DEBUG,
    )


if __name__ == "__main__":
    main()
