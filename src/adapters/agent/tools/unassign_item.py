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
    """
    Убрать LineItem из назначенных пользователю.
    Через LineItem тебе необходимо указать:
    1. Название блюда
    2. количество блюда(Например, если человек говорит что он ел блюдо не один,
    а с кем-то то можно убрать 0.5 блюда и записать 0.5 блюда другому человеку)
    3. Цену блюда(берется из списка назначенных)
    """
    return UnassignItemAction(runtime)(**kwds)
