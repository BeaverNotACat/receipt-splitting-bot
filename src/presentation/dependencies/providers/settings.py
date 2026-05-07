from dishka import Provider, Scope, provide

from src.settings import (
    AgentCheckpointerSettings,
    DatabaseSettings,
    GlobalSettings,
    KeyValueSettings,
    OpenRouterSettings,
    ReceiptLockSettings,
    TelegramSettings,
)


class SettingsProvider(Provider):
    scope = Scope.APP

    @provide
    @staticmethod
    def get_agent_checkpointr() -> AgentCheckpointerSettings:
        return AgentCheckpointerSettings()

    @provide
    @staticmethod
    def get_database() -> DatabaseSettings:
        return DatabaseSettings()

    @provide
    @staticmethod
    def get_globals() -> GlobalSettings:
        return GlobalSettings()

    @provide
    @staticmethod
    def get_key_value() -> KeyValueSettings:
        return KeyValueSettings()

    @provide
    @staticmethod
    def get_open_router() -> OpenRouterSettings:
        return OpenRouterSettings()

    @provide
    @staticmethod
    def get_receipt_lock() -> ReceiptLockSettings:
        return ReceiptLockSettings()

    @provide
    @staticmethod
    def get_telegram() -> TelegramSettings:
        return TelegramSettings()
