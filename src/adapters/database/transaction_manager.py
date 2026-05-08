from sqlalchemy.ext.asyncio import AsyncSession

from src.application.common.database.transaction_manager import (
    TransactionManagerI,
)


class TransactionManager(TransactionManagerI):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def commit(self) -> None:
        await self.session.commit()

    async def release(self) -> None:
        await self.session.rollback()
