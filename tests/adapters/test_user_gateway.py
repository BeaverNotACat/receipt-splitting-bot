from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.adapters.database.user_gateway import UserGateway
    from src.domain.models.user import RealUser
    from tests.mocks.domain import RealUserFactory


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
    updated_user = real_user_factory.build(initial_user.id)

    await user_gateway.save_user(initial_user)
    await user_gateway.save_user(updated_user)

    saved_user = await user_gateway.fetch_user(id=updated_user.id)
    assert saved_user.id == updated_user.id
    assert saved_user.nickname == updated_user.nickname
    assert getattr(saved_user, "chat_id") == updated_user.chat_id  # noqa: B009 DummyUser doesn't have chat_id
