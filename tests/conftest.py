from polyfactory.pytest_plugin import register_fixture

from tests.mocks.domain import (
    DummyUserFactory,
    LineItemFactory,
    RealUserFactory,
    ReceiptFactory,
    dummy_user,
    line_item,
    real_user,
    receipt,
)

register_fixture(DummyUserFactory)
register_fixture(LineItemFactory)
register_fixture(RealUserFactory)
register_fixture(ReceiptFactory)


__all__ = [
    "dummy_user",
    "line_item",
    "real_user",
    "receipt",
]
