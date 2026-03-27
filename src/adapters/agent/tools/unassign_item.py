from langchain.messages import ToolMessage
from langchain.tools import tool
from langgraph.types import Command

from src.domain.exceptions import DomainError
from src.domain.value_objects import LineItem, UserID

from .base import EmptyGoTo, ModifyReceiptRuntime


@tool
def unassign_item(
    runtime: ModifyReceiptRuntime,
    item: LineItem,
    user_id: UserID,
) -> Command[EmptyGoTo]:
    """
    Убрать LineItem из назначенных пользователю.
    Через LineItem тебе необходимо указать:
    1. Название блюда
    2. количество блюда(Например, если человек говорит что он ел блюдо не один,
    а с кем-то то можно убрать 0.5 блюда и записать 0.5 блюда другому человеку)
    3. Цену блюда(берется из списка назначенных)
    """
    receipt = runtime.state["receipt"]
    user = runtime.context["user_id_mapping"][user_id]
    try:
        receipt.unassign_item(item, user)
        message_text = "Successfully updated receipt"
    except (DomainError, KeyError) as err:
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
