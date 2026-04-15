from typing import Any

from aiogram_dialog import DialogManager, ShowMode, Window
from aiogram_dialog.widgets.text import Jinja
from dishka import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.receipt.form_bills import FormBills, FormBillsDTO
from src.presentation.telegram import states

from .common import (
    add_dummy_user_button,
    return_to_profile_button,
    show_bill_button,
    user_prompt_input,
)

bills_text = Jinja("""
<b>СЧЕТА:</b>
{% for nickname, bill in bills %}
{% if nickname is none %}
<b>Не назначеные товары:</b>
{% else %}
<b>{{nickname}}:</b>
{% endif %}
Название \t К-во \t Цена \t Сумма
{% for item in bill.items %}
{{item.name}}\t{{item.amount}}\t{{item.price|round(2)}}\t{{item.price*item.amount|round(2)}}
{% endfor %}
Итого: {{bill.total|round(2)}}\n
{% endfor %}
""")


@inject
async def bills_getter(
    dialog_manager: DialogManager,
    form_bill: FromDishka[FormBills],
    **_kwargs: dict[str, Any],
) -> dict[str, Any]:
    dto = FormBillsDTO(receipt_id=states.get_receipt_id(dialog_manager))
    bills_mapping = await form_bill(dto)
    await dialog_manager.switch_to(
        states.ReceiptChatSG.chat, show_mode=ShowMode.SEND
    )
    return {"bills": bills_mapping}


bills_window = Window(
    bills_text,
    add_dummy_user_button,
    show_bill_button,
    return_to_profile_button,
    user_prompt_input,
    parse_mode="HTML",
    state=states.ReceiptChatSG.bills,
    getter=bills_getter,
)
