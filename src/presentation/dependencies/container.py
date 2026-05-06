from dishka import make_async_container
from dishka.integrations.aiogram import AiogramProvider

from src.presentation.dependencies.providers import (
    AlchemyProvider,
    AuthProvider,
    CheckpointerProvider,
    KeyValueProvider,
    LangChainProvider,
    SettingsProvider,
    interactors_provider,
    repositories_provider,
    services_provider,
)

container = make_async_container(
    CheckpointerProvider(),
    AlchemyProvider(),
    AuthProvider(),
    AiogramProvider(),
    LangChainProvider(),
    KeyValueProvider(),
    SettingsProvider(),
    interactors_provider,
    repositories_provider,
    services_provider,
)
