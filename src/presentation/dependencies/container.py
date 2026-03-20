from dishka import make_async_container
from dishka.integrations.aiogram import AiogramProvider

from src.presentation.dependencies.providers import (
    AlchemyProvider,
    AuthProvider,
    SettingsProvider,
    interactors_provider,
    repositories_provider,
    services_provider,
)

container = make_async_container(
    AiogramProvider(),
    SettingsProvider(),
    services_provider,
    AlchemyProvider(),
    repositories_provider,
    AuthProvider(),
    interactors_provider,
)
