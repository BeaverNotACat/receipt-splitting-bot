from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from langgraph.checkpoint.base import BaseCheckpointSaver

from src.adapters.agent.checkpointer import (
    construct_memory_checkpointer,
    construct_postgres_checkpointer,
)
from src.settings.agent_checkpointer import AgentCheckpointerSettings


class CheckpointerProvider(Provider):
    scope = Scope.APP

    @provide
    @staticmethod
    async def get_checkpointer(
        settings: AgentCheckpointerSettings,
    ) -> AsyncIterable[BaseCheckpointSaver[str]]:
        if settings.DSN is None:
            yield construct_memory_checkpointer()
        else:
            async with construct_postgres_checkpointer(
                str(settings.DSN)
            ) as checkpointer:
                await checkpointer.setup()
                yield checkpointer
