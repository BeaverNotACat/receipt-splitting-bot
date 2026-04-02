from typing import TYPE_CHECKING

import pytest

from src.application.common.database.user_gateway import UserNotFoundError

if TYPE_CHECKING:
    from collections.abc import Callable, Coroutine
    from typing import Any

    from src.adapters.database.user_gateway import UserGateway
    from src.domain.models.user import DummyUser, RealUser
    from tests.mocks.domain import RealUserFactory

    SetupUsers = Callable[[], Coroutine[Any, Any, list[RealUser]]]


USERS_BATCH_SIZE = 10


@pytest.fixture
def setup_users(
    real_user_factory: RealUserFactory, user_gateway: UserGateway
) -> SetupUsers:
    async def setup_users_service() -> list[RealUser]:
        users = real_user_factory.batch(USERS_BATCH_SIZE)
        for user in users:
            await user_gateway.save_user(user)
        return users

    return setup_users_service


async def test_user_saving(
    real_user: RealUser, user_gateway: UserGateway
) -> None:
    await user_gateway.save_user(real_user)

    saved_user = await user_gateway.fetch_user(id=real_user.id)
    assert saved_user.id == real_user.id
    assert saved_user.nickname == real_user.nickname
    assert getattr(saved_user, "chat_id") == real_user.chat_id  # noqa: B009 DummyUser doesn't have chat_id


async def test_user_updating(
    real_user_factory: RealUserFactory, user_gateway: UserGateway
) -> None:
    initial_user = real_user_factory.build()
    await user_gateway.save_user(initial_user)
    updated_user = real_user_factory.build(initial_user.id)

    await user_gateway.save_user(updated_user)

    saved_user = await user_gateway.fetch_user(id=updated_user.id)
    assert saved_user.id == updated_user.id
    assert saved_user.nickname == updated_user.nickname
    assert getattr(saved_user, "chat_id") == updated_user.chat_id  # noqa: B009 DummyUser doesn't have chat_id


async def test_fetching_nonexisting_user(
    real_user: RealUser, user_gateway: UserGateway
) -> None:
    with pytest.raises(UserNotFoundError):
        await user_gateway.fetch_user(id=real_user.id)


async def test_fetching_dummy_user(
    dummy_user: DummyUser, user_gateway: UserGateway
) -> None:
    await user_gateway.save_user(dummy_user)

    saved_user = await user_gateway.fetch_user(id=dummy_user.id)
    assert saved_user.id == dummy_user.id
    assert saved_user.nickname == dummy_user.nickname


async def test_user_filtering(
    setup_users: SetupUsers, user_gateway: UserGateway
) -> None:
    initial_users = await setup_users()
    initial_ids = tuple(user.id for user in initial_users)

    fetched_users = await user_gateway.fetch_users(ids=initial_ids)

    assert len(initial_users) == len(fetched_users)
    for user in fetched_users:
        assert user.id in initial_ids
