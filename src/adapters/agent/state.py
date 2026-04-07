from typing import Annotated, Any, Required, TypedDict

from langchain.agents import AgentState
from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages

from src.domain.models import Receipt, User
from src.domain.value_objects import UserID

NoStructuredResponse = type(None)


def receipt_reducer(
    _current_receipt: Receipt, updated_receipt: Receipt
) -> Receipt:
    # Agent invokes with max_concurency=1 so race_condition not possible
    # But langchain's LastValue reducer invokes error to prevent races
    # Custom reducer is a workaround
    return updated_receipt


class InvokeState(TypedDict):
    messages: Required[
        Annotated[list[AnyMessage | dict[str, Any]], add_messages]
    ]
    current_user_id: UserID
    receipt: Required[Receipt]
    users: Required[list[User]]


class ReceiptModificationState(AgentState[NoStructuredResponse]):
    current_user_id: UserID
    receipt: Annotated[Required[Receipt], receipt_reducer]
    users: Required[list[User]]
