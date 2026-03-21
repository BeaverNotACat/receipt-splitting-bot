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
    """
    Убрать LineItem из неназначенных.

    Пример использования: пользователь говорит
    что они впринципе не заказывали такое блюдо

    Через LineItem тебе необходимо указать:
    1. Название блюда
    2. количество блюда
    3. Цену блюда(берется из списка неназначенных)
    """
    return RemoveItemAction(runtime)(**kwds)
