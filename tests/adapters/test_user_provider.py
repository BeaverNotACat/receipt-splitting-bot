import pytest

from src.adapters.database.user_gateway import UserGateway
from src.adapters.user_provider import UserProvider
from src.application.common.user_provider import NoActiveUserError
from src.domain.models.user import RealUser
from tests.adapters.asserts import assert_user


async def test_user_provider(
    real_user: RealUser,
    user_provider_class: type[UserProvider],
    user_gateway: UserGateway,
) -> None:
    await user_gateway.save_user(real_user)
    provider = user_provider_class(user_gateway, real_user.chat_id)

    fetched_user = await provider.fetch_current_user()

    assert_user(real_user, fetched_user)


async def test_no_chat_id(
    user_provider_class: type[UserProvider],
    user_gateway: UserGateway,
) -> None:
    provider = user_provider_class(user_gateway, None)

    with pytest.raises(NoActiveUserError):
        await provider.fetch_current_user()


async def test_nonexistent_user_fetching(
    real_user: RealUser,
    user_provider_class: type[UserProvider],
    user_gateway: UserGateway,
) -> None:
    provider = user_provider_class(user_gateway, real_user.chat_id)

    with pytest.raises(NoActiveUserError):
        await provider.fetch_current_user()
