from typing import Unpack

from langchain.tools import ToolRuntime, tool
from langgraph.types import Command
from langgraph.typing import ContextT

from .base import (
    EmptyGoTo,
    ReceiptModificationState,
    ReceiptToolActionBase,
    UnassignedItemActionInput,
)


class RemoveItemAction(ReceiptToolActionBase[*UnassignedItemActionInput]):
    def action(self, **kwds: Unpack[UnassignedItemActionInput]) -> None:
        return self.receipt.remove_item(**kwds)


@tool
def remove_item(
    runtime: ToolRuntime[ContextT, ReceiptModificationState],
    **kwds: Unpack[UnassignedItemActionInput],
) -> Command[EmptyGoTo]:
    return RemoveItemAction(runtime)(**kwds)
