from typing import TYPE_CHECKING, Self

from src.application.common.database.transaction_manager import (
    TransactionManagerI,
)

if TYPE_CHECKING:
    from types import TracebackType


class FakeTransactionManager(TransactionManagerI):
    def __init__(self) -> None: ...

    async def commit(self) -> None: ...

    async def rollback(self) -> None: ...

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc_value: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None: ...
