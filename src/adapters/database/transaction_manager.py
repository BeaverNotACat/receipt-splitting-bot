from typing import TYPE_CHECKING, Self

from sqlalchemy.ext.asyncio import AsyncSession  # noqa: TC002

from src.application.common.database.transaction_manager import (
    TransactionManagerI,
)

if TYPE_CHECKING:
    from types import TracebackType


class TransactionManager(TransactionManagerI):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        await self.session.rollback()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()
