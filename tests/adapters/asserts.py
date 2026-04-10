from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.domain.models import Receipt, User


def assert_receipt(initial_receipt: Receipt, new_receipt: Receipt) -> None:
    assert new_receipt.id == initial_receipt.id
    assert new_receipt.created_at == initial_receipt.created_at
    assert new_receipt.title == initial_receipt.title
    assert new_receipt.creditor_id == initial_receipt.creditor_id
    assert len(new_receipt.unassigned_items) == len(
        initial_receipt.unassigned_items
    )
    for item in new_receipt.unassigned_items:
        assert item in initial_receipt.unassigned_items
    assert new_receipt.assignees.keys() == initial_receipt.assignees.keys()
    for user_id in initial_receipt.assignees:
        for item in initial_receipt.assignees[user_id]:
            assert item in new_receipt.assignees[user_id]


def assert_user(initial_user: User, new_user: User) -> None:
    assert initial_user.id == new_user.id
    assert initial_user.nickname == new_user.nickname
    assert getattr(initial_user, "chat_id", None) == getattr(
        new_user, "chat_id", None
    )
