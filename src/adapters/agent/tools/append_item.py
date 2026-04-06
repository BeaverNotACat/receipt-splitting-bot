from langchain.messages import ToolMessage
from langchain.tools import tool
from langgraph.types import Command

from src.domain.exceptions import DomainError
from src.domain.value_objects import LineItem

from .base import EmptyGoTo, ModifyReceiptRuntime


@tool
def append_item(
    runtime: ModifyReceiptRuntime, item: LineItem
) -> Command[EmptyGoTo]:
    """
    Добавить LineItem в неназначенные.
    Через LineItem тебе необходимо указать:
    1. Название блюда
    2. количество блюда
    3. Цену блюда(берется из чека)
    """
    receipt = runtime.state["receipt"]

    try:
        receipt.append_item(item)
        message_text = "Successfully updated receipt"
    except DomainError as err:
        message_text = f"Failed to update receipt: {err!s}"
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
