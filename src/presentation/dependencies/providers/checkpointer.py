from collections.abc import AsyncIterable

from dishka import Provider, Scope, provide
from langgraph.checkpoint.base import BaseCheckpointSaver

from src.adapters.agent.checkpointer import construct_checkpointer
from src.settings.agent_checkpointer import AgentCheckpointerSettings


class CheckpointerProvider(Provider):
    scope = Scope.APP

    @provide
    @staticmethod
    async def get_checkpointer(
        settings: AgentCheckpointerSettings,
    ) -> AsyncIterable[BaseCheckpointSaver[str]]:
        async with construct_checkpointer(str(settings.DSN)) as checkpointer:
            await checkpointer.setup()
            yield checkpointer
