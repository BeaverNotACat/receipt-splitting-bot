from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from src.application.onboard import OnboardUser


@pytest.fixture
def onboard_user_iteractor() -> OnboardUser:
    raise NotImplementedError
