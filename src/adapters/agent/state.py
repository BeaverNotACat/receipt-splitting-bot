from typing import Annotated, Any, Required, TypedDict

from langchain.agents import AgentState
from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages

from src.domain.models import BaseUserData, ReceiptItemsData

NoStructuredResponse = type(None)


class InvokeState(TypedDict):
    receipt_items_data: Required[ReceiptItemsData]
    users: Required[tuple[BaseUserData, ...]]
    messages: Required[
        Annotated[list[AnyMessage | dict[str, Any]], add_messages]
    ]


class ReceiptModificationState(AgentState[NoStructuredResponse]):
    receipt_items_data: Required[ReceiptItemsData]
    users: Required[tuple[BaseUserData, ...]]
