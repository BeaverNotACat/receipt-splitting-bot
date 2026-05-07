from contextlib import _AsyncGeneratorContextManager

from langgraph.checkpoint.memory import InMemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer

serde = JsonPlusSerializer(
    allowed_msgpack_modules=(
        ("src.domain.models", "Receipt"),
        ("src.domain.models", "RealUser"),
        ("src.domain.models", "DummyUser"),
        ("src.domain.value_objects", "LineItem"),
    ),
)


def construct_postgres_checkpointer(
    conn_string: str,
) -> _AsyncGeneratorContextManager[AsyncPostgresSaver, None]:
    return AsyncPostgresSaver.from_conn_string(
        conn_string, pipeline=True, serde=serde
    )


def construct_memory_checkpointer() -> InMemorySaver:
    return InMemorySaver(serde=serde)
