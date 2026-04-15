from typing import TYPE_CHECKING

import pytest
from polyfactory.factories import DataclassFactory
from polyfactory.pytest_plugin import register_fixture

from src.application.real_user.change_nickname import (
    ChangeNickname,
    ChangeNicknameDTO,
)
from src.application.real_user.register import (
    RegisterUser,
    RegisterUserDTO,
)
from src.domain.services.user import UserService
from tests.application.fakes.fake_transaction_manager import (
    FakeTransactionManager,
)
from tests.application.fakes.fake_user_gateway import FakeUserGateway
from tests.application.fakes.fake_user_provider import FakeUserProvider

if TYPE_CHECKING:
    from src.domain.models.user import RealUser


@register_fixture
class RegisterUserDTOFactory(DataclassFactory[RegisterUserDTO]): ...


@register_fixture
class ChangeNicknameDTOFactory(DataclassFactory[ChangeNicknameDTO]): ...


@pytest.fixture
def fake_user_gateway() -> FakeUserGateway:
    return FakeUserGateway()


@pytest.fixture
def fake_user_provider(real_user: RealUser) -> FakeUserProvider:
    return FakeUserProvider(real_user)


@pytest.fixture
def register_user_dto(
    register_user_dto_factory: RegisterUserDTOFactory,
) -> RegisterUserDTO:
    return register_user_dto_factory.build()


@pytest.fixture
def change_nickname_dto(
    change_nickname_dto_factory: ChangeNicknameDTOFactory,
    register_user_dto: RegisterUserDTO,
) -> ChangeNicknameDTO:
    return change_nickname_dto_factory.build(
        nickname=register_user_dto.nickname,
    )


@pytest.fixture
def register_user_interactor(
    fake_user_gateway: FakeUserGateway,
) -> RegisterUser:
    return RegisterUser(
        FakeTransactionManager(), UserService(), fake_user_gateway
    )


@pytest.fixture
def change_nickname_interactor(
    fake_user_gateway: FakeUserGateway,
    fake_user_provider: FakeUserProvider,
) -> ChangeNickname:
    return ChangeNickname(
        FakeTransactionManager(),
        fake_user_gateway,
        fake_user_provider,
    )


async def test_change_nicknamfetch_usere(
    register_user_dto: RegisterUserDTO,
    register_user_interactor: RegisterUser,
    change_nickname_dto: ChangeNicknameDTO,
    change_nickname_interactor: ChangeNickname,
    fake_user_gateway: FakeUserGateway,
) -> None:
    await register_user_interactor(register_user_dto)
    await change_nickname_interactor(change_nickname_dto)

    saved_user = next(iter(fake_user_gateway.users_storage.values()))
    assert saved_user.nickname == change_nickname_dto.nickname
