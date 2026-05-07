from langchain.messages import ToolMessage
from langchain.tools import tool
from langgraph.types import Command

from src.adapters.agent.templating import show_receipt_tool_prompt_template

from .base import EmptyGoTo, ModifyReceiptRuntime


@tool
def show_receipt(runtime: ModifyReceiptRuntime) -> Command[EmptyGoTo]:
    """
    Узнать текущее состояние чека.
    - Текущего пользователя
    - Список пользователей
    - неназначенные товары
    - назначения товаров
    """
    receipt = runtime.state["receipt"]

    bills = [
        (user_id, receipt.form_bill(user_id))
        for user_id in [*receipt.participants_ids, None]
    ]
    text = show_receipt_tool_prompt_template.render(
        current_user_id=runtime.state["current_user_id"],
        user_id_mapping=runtime.context["user_id_mapping"],
        bills=bills,
    )
    return Command(
        update={
            "messages": [
                ToolMessage(
                    text,
                    tool_call_id=runtime.tool_call_id,
                )
            ],
        }
    )
