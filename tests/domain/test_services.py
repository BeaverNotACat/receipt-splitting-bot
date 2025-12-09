from typing import TYPE_CHECKING

from src.domain.services.receipt import create_receipt
from src.domain.services.user import create_dummy_user, create_real_user
from tests.domain.asserts import assert_new_receipt_creation

if TYPE_CHECKING:
    from faker import Faker

    from tests.dataset.domain import DummyUserFactory, RealUserFactory


def test_new_real_user_creation(real_user_factory: RealUserFactory) -> None:
    mock_user = real_user_factory.build()

    user = create_real_user(
        telegram_id=mock_user.telegram_id, name=mock_user.name
    )

    assert user.id
    assert user.name == mock_user.name
    assert user.telegram_id == mock_user.telegram_id


def test_new_dummy_user_creation(dummy_user_factory: DummyUserFactory) -> None:
    mock_user = dummy_user_factory.build()

    user = create_dummy_user(name=mock_user.name)

    assert user.id
    assert user.name == mock_user.name


def test_new_receipt_creation(
    real_user_factory: RealUserFactory, faker: Faker
) -> None:
    creditor = real_user_factory.build()
    title = faker.pystr(max_chars=50)

    receipt = create_receipt(creditor=creditor, title=title)

    assert_new_receipt_creation(receipt, creditor.id, title)
