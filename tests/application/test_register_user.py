import pytest
from polyfactory.factories import DataclassFactory
from polyfactory.pytest_plugin import register_fixture

from src.application.real_user.register import (
    RegisterUser,
    RegisterUserDTO,
)
from src.domain.services.user import UserService
from tests.application.fakes.fake_transaction_manager import (
    FakeTransactionManager,
)
from tests.application.fakes.fake_user_gateway import FakeUserGateway


@register_fixture
class RegisterUserDTOFactory(DataclassFactory[RegisterUserDTO]): ...


@pytest.fixture
def fake_user_gateway() -> FakeUserGateway:
    return FakeUserGateway()


@pytest.fixture
def register_user_dto(
    register_user_dto_factory: RegisterUserDTOFactory,
) -> RegisterUserDTO:
    return register_user_dto_factory.build()


@pytest.fixture
def register_user_interactor(
    fake_user_gateway: FakeUserGateway,
) -> RegisterUser:
    return RegisterUser(
        FakeTransactionManager(), UserService(), fake_user_gateway
    )


@pytest.mark.asyncio
async def test_onboard_user(
    register_user_dto: RegisterUserDTO,
    register_user_interactor: RegisterUser,
    fake_user_gateway: FakeUserGateway,
) -> None:
    await register_user_interactor(register_user_dto)

    saved_user = next(iter(fake_user_gateway.users_storage.values()))
    assert saved_user.nickname == register_user_dto.nickname
