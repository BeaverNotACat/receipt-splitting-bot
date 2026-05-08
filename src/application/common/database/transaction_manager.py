from abc import abstractmethod
from typing import Protocol


class TransactionManagerI(Protocol):
    """
    DB transactions manager, transcations autostarts with query
    Essential for external pooler connection management
    """

    @abstractmethod
    async def commit(self) -> None:
        """
        Commit changes and return connection into pool
        """
        raise NotImplementedError

    @abstractmethod
    async def release(self) -> None:
        """
        Rollbacks changes and return connection into pool
        """
        raise NotImplementedError
