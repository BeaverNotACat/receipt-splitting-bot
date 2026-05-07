from dishka import Provider, Scope, provide
from langgraph.checkpoint.base import BaseCheckpointSaver
from psycopg.rows import dict_row
from psycopg_pool import AsyncConnectionPool

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
    ) -> BaseCheckpointSaver[str]:
        if settings.DSN is None:
            return construct_memory_checkpointer()

        pool = AsyncConnectionPool(
            str(settings.DSN),
            kwargs={"autocommit": True, "row_factory": dict_row},
        )

        checkpointer = construct_postgres_checkpointer(pool)  # type: ignore[arg-type]
        await checkpointer.setup()
        return checkpointer
