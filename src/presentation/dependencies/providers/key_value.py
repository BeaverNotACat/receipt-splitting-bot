from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from src.adapters.locks import ReceiptLock
from src.application.common.locks import ReceiptLockI
from src.settings import KeyValueSettings, ReceiptLockSettings


class KeyValueProvider(Provider):
    scope = Scope.APP

    @provide
    @staticmethod
    def get_redis_client(settings: KeyValueSettings) -> Redis:
        return Redis.from_url(str(settings.DSN))

    @provide
    @staticmethod
    def get_receipt_lock(
        client: Redis, settings: ReceiptLockSettings
    ) -> ReceiptLockI:
        return ReceiptLock(client, settings.PREFIX, settings.LIFETIME)
