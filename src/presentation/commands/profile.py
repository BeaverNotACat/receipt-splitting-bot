from typing import Any
from uuid import UUID

from aiogram import F
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
from src.application.receipt.list import ListReceipts
from src.domain.value_objects import ReceiptID

from . import states

PAGE_SIZE = 4


@inject
async def user_profile_getter(
    dialog_manager: DialogManager,
    user_provider: FromDishka[UserProviderI],
    list_receipts: FromDishka[ListReceipts],
    **_kwargs: dict[str, Any],
) -> dict[str, Any]:
    scroll: ManagedScroll = dialog_manager.find("scroll")
    page = await scroll.get_page()
    offset = page * PAGE_SIZE
    limit = offset + PAGE_SIZE

    user = await user_provider.fetch_current_user()
    receipts = await list_receipts(None)

    return {
        "nickname": user.nickname,
        "total": len(receipts),
        "pages": len(receipts) // PAGE_SIZE + bool(len(receipts) % PAGE_SIZE),
        "receipts": receipts[offset:limit],
    }


profile_dialog = Dialog(
    Window(
        Format("Добро пожаловать, {nickname}"),
        Format(
            "У вас есть {total} чеков, нажмите на один, чтобы открыть",
            when=F["total"],
        ),
        Const(
            "Пока что у вас нет чеков, создайте первый кнопкой ниже",
            when=~F["total"],
        ),
        StubScroll(id="scroll", pages=F["pages"]),
        Start(
            Const("➕ Создать чек"),
            id="new",
            state=states.CreateReceiptSG.title,
        ),
        Column(
            Select(
                Format("{item.title}"),
                item_id_getter=lambda item: item.id,
                type_factory=lambda x: ReceiptID(UUID(x)),
                items="receipts",
                id="list",
            ),
        ),
        NumberedPager(id="pager", scroll="scroll"),
        state=states.ProfileSG.view,
        getter=user_profile_getter,
    )
)
