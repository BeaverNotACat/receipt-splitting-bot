from src.application.common.database.transaction_manager import (
    TransactionManagerI,
)


class FakeTransactionManager(TransactionManagerI):
    def __init__(self) -> None: ...

    async def commit(self) -> None: ...

    async def release(self) -> None: ...
