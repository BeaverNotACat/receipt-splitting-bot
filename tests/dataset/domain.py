from polyfactory.factories import DataclassFactory

from src.domain.models.receipt import Receipt
from src.domain.models.user import DummyUser, RealUser
from src.domain.value_objects import LineItem


class RealUserFactory(DataclassFactory[RealUser]):
    @classmethod
    def name(cls) -> str:
        return cls.__faker__.name()


class DummyUserFactory(DataclassFactory[DummyUser]):
    @classmethod
    def name(cls) -> str:
        return cls.__faker__.name()


class LineItemFactory(DataclassFactory[LineItem]): ...


class ReceiptFactory(DataclassFactory[Receipt]): ...
