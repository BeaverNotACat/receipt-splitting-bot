from typing import TYPE_CHECKING

from src.domain.value_objects import ReceiptTitle
from tests.domain.asserts import assert_new_receipt_creation

if TYPE_CHECKING:
    from faker import Faker

    from src.domain.services import ReceiptService, UserService
    from tests.mocks.domain import DummyUserFactory, RealUserFactory


def test_new_real_user_creation(
    real_user_factory: RealUserFactory, user_service: UserService
) -> None:
    mock_user = real_user_factory.build()

    user = user_service.create_real_user(
        chat_id=mock_user.chat_id, nickname=mock_user.nickname
    )

    assert user.id
    assert user.nickname == mock_user.nickname
    assert user.chat_id == mock_user.chat_id


def test_new_dummy_user_creation(
    dummy_user_factory: DummyUserFactory, user_service: UserService
) -> None:
    mock_user = dummy_user_factory.build()

    user = user_service.create_dummy_user(nickname=mock_user.nickname)

    assert user.id
    assert user.nickname == mock_user.nickname


def test_new_receipt_creation(
    real_user_factory: RealUserFactory,
    faker: Faker,
    receipt_service: ReceiptService,
) -> None:
    creditor = real_user_factory.build()
    title = ReceiptTitle(faker.pystr(max_chars=50))

    receipt = receipt_service.create_receipt(creditor=creditor, title=title)

    assert_new_receipt_creation(receipt, creditor.id, title)
