from dishka import make_async_container
from dishka.integrations.aiogram import AiogramProvider

from src.presentation.dependencies.providers import (
    AlchemyProvider,
    AuthProvider,
    LangChainProvider,
    SettingsProvider,
    interactors_provider,
    repositories_provider,
    services_provider,
)

container = make_async_container(
    AlchemyProvider(),
    AuthProvider(),
    AiogramProvider(),
    LangChainProvider(),
    SettingsProvider(),
    interactors_provider,
    repositories_provider,
    services_provider,
)
