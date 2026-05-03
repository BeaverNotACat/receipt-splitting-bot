from typing import Any, cast
from uuid import UUID

from aiogram import F
from aiogram.types import CallbackQuery
from aiogram_dialog import Dialog, DialogManager, Window
from aiogram_dialog.widgets.common import ManagedScroll
from aiogram_dialog.widgets.kbd import (
    Column,
    NumberedPager,
    Select,
    Start,
    StubScroll,
)
from aiogram_dialog.widgets.text import Const, Format
from dishka.integrations.aiogram import FromDishka
from dishka.integrations.aiogram_dialog import inject

from src.application.common.user_provider import UserProviderI
from src.application.receipt.list import ListReceipts, ListReceiptsDTO
from src.domain.value_objects import (
    LimitOffsetPagination,
    ReceiptID,
)

from . import states

PAGE_SIZE = 4
NICKNAME_INPUT_ID = "nickname"


def get_correct_receipt_wording(total: int) -> str:
    if 11 <= total % 100 <= 14:  # noqa: PLR2004
        return "чеков"

    last_digit = total % 10
    if last_digit == 1:
        return "чек"
    if 2 <= last_digit <= 4:  # noqa: PLR2004
        return "чека"

    return "чеков"


@inject
async def user_profile_getter(
    dialog_manager: DialogManager,
    user_provider: FromDishka[UserProviderI],
    list_receipts: FromDishka[ListReceipts],
    **_kwargs: dict[str, Any],
) -> dict[str, Any]:
    scroll: ManagedScroll = cast(ManagedScroll, dialog_manager.find("scroll"))
    page = await scroll.get_page()
    pagination = LimitOffsetPagination(
        offset=page * PAGE_SIZE,
        limit=PAGE_SIZE,
    )

    dto = await list_receipts(ListReceiptsDTO(pagination=pagination))
    user = await user_provider.fetch_current_user()
    return {
        "nickname": user.nickname,
        "total": dto.total,
        "pages": dto.total // PAGE_SIZE + bool(dto.total % PAGE_SIZE),
        "receipts": dto.receipts,
        "receipt_wording": get_correct_receipt_wording(dto.total),
    }


async def on_selected(
    _event: CallbackQuery,
    _select: Select[Any],
    dialog_manager: DialogManager,
    receipt_id: ReceiptID,
) -> None:
    await states.start_receipt_chat(dialog_manager, receipt_id)


show_profile_dialog = Dialog(
    Window(
        Format("Добро пожаловать, {nickname}"),
        Format(
            "У вас есть {total} {receipt_wording}. Вы можете нажать на один, "
            "чтобы открыть диалог с агентом",
            when=F["total"],
        ),
        Const(
            "Пока что у вас нет чеков, создайте первый",
            when=~F["total"],
        ),
        StubScroll(id="scroll", pages=F["pages"]),
        Start(
            Const("📝 Изменить имя"),
            id="change_nickname",
            state=states.ChangeNicknameSG.nickname,
        ),
        Start(
            Const("➕ Создать чек"),
            id="create",
            state=states.CreateReceiptSG.title,
        ),
        Column(
            Select(
                Format("{item.title}"),
                item_id_getter=lambda item: item.id,
                type_factory=lambda x: ReceiptID(UUID(x)),
                items="receipts",
                id="list",
                on_click=on_selected,
            ),
        ),
        NumberedPager(
            id="pager",
            scroll="scroll",
            when=F["pages"] > 1,
        ),
        state=states.ProfileSG.view,
        getter=user_profile_getter,
        preview_add_transitions=[
            Start(Const("0"), id="0", state=states.ReceiptChatSG.greeting),
        ],
    ),
)
