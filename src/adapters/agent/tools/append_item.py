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


class AppendItemAction(ReceiptToolActionBase[*UnassignedItemActionInput]):
    def action(self, **kwds: Unpack[UnassignedItemActionInput]) -> None:
        return self.receipt.append_item(**kwds)


@tool
def append_item(
    runtime: ToolRuntime[ContextT, ReceiptModificationState],
    **kwds: Unpack[UnassignedItemActionInput],
) -> Command[EmptyGoTo]:
    """
    Добавить LineItem в неназначенные.
    Через LineItem тебе необходимо указать:
    1. Название блюда
    2. количество блюда
    3. Цену блюда(берется из запроса пользователя)
    """
    return AppendItemAction(runtime)(**kwds)
