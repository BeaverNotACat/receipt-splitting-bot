from typing import Annotated, Any, Required, TypedDict

from langchain.agents import AgentState
from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages

from src.domain.models import BaseUserData, ReceiptItemsData
from src.domain.value_objects import UserID

NoStructuredResponse = type(None)


class InvokeState(TypedDict):
    messages: Required[
        Annotated[list[AnyMessage | dict[str, Any]], add_messages]
    ]
    current_user_id: UserID
    receipt_items_data: Required[ReceiptItemsData]
    users: Required[tuple[BaseUserData, ...]]


class ReceiptModificationState(AgentState[NoStructuredResponse]):
    current_user_id: UserID
    receipt_items_data: Required[ReceiptItemsData]
    users: Required[tuple[BaseUserData, ...]]
