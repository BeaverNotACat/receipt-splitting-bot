from polyfactory.pytest_plugin import register_fixture

from tests.dataset.domain import (
    DummyUserFactory,
    LineItemFactory,
    RealUserFactory,
    ReceiptFactory,
)

register_fixture(DummyUserFactory)
register_fixture(LineItemFactory)
register_fixture(RealUserFactory)
register_fixture(ReceiptFactory)
