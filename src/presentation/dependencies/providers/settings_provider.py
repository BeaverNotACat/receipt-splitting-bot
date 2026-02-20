from dishka import Provider, Scope, provide

from src.settings import Settings


class SettingsProvider(Provider):
    scope = Scope.APP

    @provide
    @staticmethod
    def get_settings() -> Settings:
        return Settings()
