from abc import abstractmethod
from contextlib import AbstractAsyncContextManager
from typing import Protocol

from src.domain.value_objects import ReceiptID


class ReceiptLockI(Protocol):
    """Mutex-like lock for order-specifit receipt manipulations"""

    @abstractmethod
    def __call__(
        self, receipt_id: ReceiptID
    ) -> AbstractAsyncContextManager[None]:
        raise NotImplementedError
