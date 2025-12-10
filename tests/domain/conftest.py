import pytest

from src.domain.services import ReceiptService, UserService


@pytest.fixture
def receipt_service() -> ReceiptService:
    return ReceiptService()


@pytest.fixture
def user_service() -> UserService:
    return UserService()
