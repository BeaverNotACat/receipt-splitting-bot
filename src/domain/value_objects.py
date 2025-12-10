from dataclasses import dataclass
from decimal import Decimal
from typing import Annotated, NewType
from uuid import UUID

from annotated_types import Gt


@dataclass(frozen=True)
class LineItem:
    """
    Receipt line
    """

    name: str
    amount: Annotated[Decimal, Gt(0)]
    price: Annotated[Decimal, Gt(0)]

    def __hash__(self) -> int:
        return hash((self.name, self.price))

    def __eq__(self, value: object, /) -> bool:
        if not isinstance(value, LineItem):
            raise NotImplementedError

        return self.name == value.name and self.price == value.price


@dataclass(frozen=True)
class Bill:
    """
    Bill to be payed by debtor user
    """

    items: tuple[LineItem]

    @property
    def total(self) -> Decimal:
        return Decimal(sum(item.price * item.amount for item in self.items))


ChatID = NewType("ChatID", int)
UserID = NewType("UserID", UUID)
ReceiptID = NewType("ReceiptID", UUID)
