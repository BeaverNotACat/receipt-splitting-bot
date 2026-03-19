from abc import ABC, abstractmethod
from typing import TypedDict

from langchain.agents import AgentState
from langchain.messages import ToolMessage
from langchain.tools import ToolRuntime
from langgraph.types import Command
from langgraph.typing import ContextT

from src.domain.exceptions import DomainError
from src.domain.models import ReceiptItemsData, User
from src.domain.value_objects import LineItem

NoStructuredResponse = type(None)
EmptyGoTo = tuple[()]


class ReceiptModificationState(AgentState[NoStructuredResponse]):
    receipt_items_data: ReceiptItemsData
    users: tuple[User, ...]


class ReceiptToolActionBase[ActionInputT](ABC):
    """
    Strategy pattern for receipt related tools
    """

    def __init__(
        self,
        runtime: ToolRuntime[ContextT, ReceiptModificationState],
    ) -> None:
        self.tool_call_id = runtime.tool_call_id
        self.receipt = runtime.state["receipt_item_info"]

    @abstractmethod
    def action(self, **kwds: ActionInputT) -> None:
        raise NotImplementedError

    def __call__(self, **kwds: ActionInputT) -> Command[EmptyGoTo]:
        """
        Calls self.action and decides tool answer on action result
        """
        try:
            self.action(**kwds)
            message_text = "Successfully updated receipt"
        except DomainError as err:
            message_text = f"Failed to update receipt: {err!s}"

        return Command(
            update={
                "receipt": self.receipt,
                "messages": [
                    ToolMessage(
                        message_text,
                        tool_call_id=self.tool_call_id,
                    )
                ],
            }
        )


class UnassignedItemActionInput(TypedDict):
    item: LineItem


class AssignedItemActionInput(TypedDict):
    item: LineItem
    user: User
