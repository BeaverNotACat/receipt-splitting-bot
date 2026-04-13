from dishka import Provider, Scope, provide
from redis.asyncio import Redis

from src.adapters.locks import ReceiptLock
from src.application.common.locks import ReceiptLockI
from src.settings import Settings


class RedisProvider(Provider):
    scope = Scope.APP

    @provide
    @staticmethod
    def get_redis_client(settings: Settings) -> Redis:
        return Redis.from_url(str(settings.KEY_VALUE_STORE_DSN))

    receipt_lock = provide(ReceiptLock, provides=ReceiptLockI)
