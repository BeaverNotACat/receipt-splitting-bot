from typing import Unpack

from langchain.tools import ToolRuntime, tool
from langgraph.types import Command
from langgraph.typing import ContextT

from .base import (
    AssignedItemActionInput,
    EmptyGoTo,
    ReceiptModificationState,
    ReceiptToolActionBase,
)


class UnassignItemAction(ReceiptToolActionBase[*AssignedItemActionInput]):
    def action(self, **kwds: Unpack[AssignedItemActionInput]) -> None:
        return self.receipt.unassign_item(**kwds)


@tool
def unassign_item(
    runtime: ToolRuntime[ContextT, ReceiptModificationState],
    **kwds: Unpack[AssignedItemActionInput],
) -> Command[EmptyGoTo]:
    return UnassignItemAction(runtime)(**kwds)
