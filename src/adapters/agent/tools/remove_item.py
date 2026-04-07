from langchain.messages import ToolMessage
from langchain.tools import tool
from langgraph.types import Command

from src.domain.exceptions import DomainError
from src.domain.value_objects import LineItem

from .base import EmptyGoTo, ModifyReceiptRuntime


@tool
def remove_item(
    runtime: ModifyReceiptRuntime,
    item: LineItem,
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
    receipt = runtime.state["receipt"]
    try:
        receipt.remove_item(item)
        message_text = "Successfully updated receipt"
    except DomainError as err:
        message_text = f"Failed to update receipt: {type(err)} {err!s}"
    return Command(
        update={
            "receipt": receipt,
            "messages": [
                ToolMessage(
                    message_text,
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )
