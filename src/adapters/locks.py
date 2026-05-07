from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from uuid import uuid4

from redis.asyncio import Redis
from redis.asyncio.client import PubSub

from src.application.common.locks import ReceiptLockI
from src.domain.value_objects import ReceiptID


class ReceiptLock(ReceiptLockI):
    def __init__(
        self, client: Redis, key_prefix: str, lock_lifetime: int
    ) -> None:
        self.client = client
        self.key_prefix = key_prefix
        self.lock_lifetime = lock_lifetime

    @asynccontextmanager
    async def __call__(self, receipt_id: ReceiptID) -> AsyncIterator[None]:
        key, token = f"{self.key_prefix}:{receipt_id}", str(uuid4())
        channel = f"{key}:channel"
        pubsub = await self.subsribe_for_unlock(channel)

        while not await self._try_set_lock(key, token):
            await pubsub.get_message(
                ignore_subscribe_messages=True, timeout=self.lock_lifetime
            )

        yield

        await self.client.delete(key)
        await self.client.publish(channel, "Released")

    async def subsribe_for_unlock(self, channel: str) -> PubSub:
        pubsub = self.client.pubsub()
        await pubsub.subscribe(channel)
        return pubsub

    async def _try_set_lock(self, key: str, token: str) -> bool:
        return bool(
            await self.client.set(key, token, nx=True, ex=self.lock_lifetime)
        )
