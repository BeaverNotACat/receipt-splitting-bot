from langchain.messages import ToolMessage
from langchain.tools import tool
from langgraph.types import Command

from src.domain.exceptions import DomainError
from src.domain.value_objects import LineItem, UserID

from .base import EmptyGoTo, ModifyReceiptRuntime


@tool
def assign_item(
    runtime: ModifyReceiptRuntime,
    item: LineItem,
    user_id: UserID,
) -> Command[EmptyGoTo]:
    """
    Назначить LineItem из неназначенных, пользователю.
    Через LineItem тебе необходимо указать:
    1. Название блюда
    2. количество блюда(Например, если 2 человека ели одно блюдо
    ты можешь назначить каждому по 0.5 этого блюда)
    3. Цену блюда(берется из списка неназначенных)
    """
    receipt = runtime.state["receipt"]
    try:
        user = runtime.context["user_id_mapping"][user_id]
        receipt.assign_item(item, user)
        message_text = "Successfully updated receipt"
    except (DomainError, KeyError) as err:
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
