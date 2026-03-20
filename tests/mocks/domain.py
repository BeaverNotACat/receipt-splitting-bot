from datetime import UTC, datetime
from decimal import Decimal

import pytest
from polyfactory.factories import DataclassFactory
from polyfactory.pytest_plugin import register_fixture

from src.domain.models.receipt import Receipt
from src.domain.models.user import DummyUser, RealUser
from src.domain.value_objects import ChatID, LineItem, UserNickname


@register_fixture
class RealUserFactory(DataclassFactory[RealUser]):
    @classmethod
    def name(cls) -> UserNickname:
        return UserNickname(cls.__faker__.name())

    @classmethod
    def chat_id(cls) -> ChatID:
        return ChatID(cls.__faker__.random_int(0, 2 << 52))


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
class LineItemFactory(DataclassFactory[LineItem]):
    __set_as_default_factory_for_type__ = True

    @classmethod
    def price(cls) -> Decimal:
        return Decimal(cls.__random__.randint(1, 10**8)) / 100

    @classmethod
    def amount(cls) -> Decimal:
        return Decimal(cls.__random__.randint(1, 10**8)) / 100


@pytest.fixture
def line_item(line_item_factory: LineItemFactory) -> LineItem:
    return line_item_factory.build()


@register_fixture
class ReceiptFactory(DataclassFactory[Receipt]):
    __randomize_collection_length__ = True
    __min_collection_length__ = 0
    __max_collection_length__ = 15

    @classmethod
    def created_at(cls) -> datetime:
        return datetime.now(UTC)


@pytest.fixture
def receipt(receipt_factory: ReceiptFactory) -> Receipt:
    receipt = receipt_factory.build()

    # TODO(beavernotat): No assignees for creditor
    # https://github.com/BeaverNotACat/receipt-splitting-bot/issues/33
    receipt.assignees[receipt.creditor_id] = []
    return receipt
