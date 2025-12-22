import pytest
from polyfactory.factories import DataclassFactory
from polyfactory.pytest_plugin import register_fixture

from src.domain.models.receipt import Receipt
from src.domain.models.user import DummyUser, RealUser
from src.domain.value_objects import LineItem


@register_fixture
class RealUserFactory(DataclassFactory[RealUser]):
    @classmethod
    def name(cls) -> str:
        return cls.__faker__.name()


@pytest.fixture
def real_user(real_user_factory: RealUserFactory) -> RealUser:
    return real_user_factory.build()


@register_fixture
class DummyUserFactory(DataclassFactory[DummyUser]):
    @classmethod
    def name(cls) -> str:
        return cls.__faker__.name()


@pytest.fixture
def dummy_user(dummy_user_factory: DummyUserFactory) -> DummyUser:
    return dummy_user_factory.build()


@register_fixture
class LineItemFactory(DataclassFactory[LineItem]): ...


@pytest.fixture
def line_item(line_item_factory: LineItemFactory) -> LineItem:
    return line_item_factory.build()


@register_fixture
class ReceiptFactory(DataclassFactory[Receipt]): ...


@pytest.fixture
def receipt(receipt_factory: ReceiptFactory) -> Receipt:
    return receipt_factory.build()
