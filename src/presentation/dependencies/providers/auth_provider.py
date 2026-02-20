from dishka import Provider, Scope, provide
from dishka.integrations.aiogram import AiogramMiddlewareData

from src.adapters.user_provider import UserProvider
from src.application.common.database.user_gateway import UserReaderI
from src.application.common.user_provider import UserProviderI
from src.domain.value_objects import ChatID


class AuthProvider(Provider):
    scope = Scope.REQUEST

    @provide
    @staticmethod
    def get_user_provider(
        user_reader: UserReaderI,
        middleware_data: AiogramMiddlewareData,
    ) -> UserProviderI:
        chat_id = None
        if user := middleware_data.get("event_from_user"):
            chat_id = ChatID(user.id)
        return UserProvider(user_reader, chat_id)
