from collections import defaultdict
from typing import TYPE_CHECKING, Unpack

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession  # noqa: TC002

from src.application.common.database.receipt_gateway import (
    MultipleReceiptsFilters,
    ReceiptReaderI,
    ReceiptSaverI,
    SingleReceiptFilters,
)
from src.domain.models.receipt import Receipt
from src.domain.value_objects import LineItem, ReceiptID, ReceiptTitle, UserID

from .orm import LineItemORM, ReceiptORM

if TYPE_CHECKING:
    from collections.abc import Iterable


class ReceiptGateway(ReceiptReaderI, ReceiptSaverI):
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def fetch_receipt(
        self, **filters: Unpack[SingleReceiptFilters]
    ) -> Receipt:
        query = select(ReceiptORM).filter_by(**filters)
        receipt_orm = await self.session.execute(query)
        return self._map_to_domain(receipt_orm.scalar_one())

    async def fetch_receipts(
        self, **filters: Unpack[MultipleReceiptsFilters]
    ) -> list[Receipt]:
        query = select(ReceiptORM).filter_by(**filters)
        receipt_orm = await self.session.execute(query)
        return self._bulk_map_to_domain(receipt_orm.scalars())

    async def save_receipt(self, receipt: Receipt) -> None:
        receipt_orm = await self._map_to_orm(receipt)
        await self.session.merge(receipt_orm)

    async def _map_to_orm(self, receipt: Receipt) -> ReceiptORM:
        return ReceiptORM(
            id=receipt.id,
            title=receipt.title,
            creditor_id=receipt.creditor_id,
            created_at=receipt.created_at,
            line_items=self._map_line_items_to_orm(receipt),
        )

    @staticmethod
    def _map_line_items_to_orm(receipt: Receipt) -> list[LineItemORM]:
        line_items = [
            LineItemORM(
                receipt_id=receipt.id,
                name=item.name,
                price=item.price,
                amount=item.amount,
                assigned_to=None,
            )
            for item in receipt.unassigned_items
        ]
        for user_id, items in receipt.assignees.items():
            line_items.extend(
                LineItemORM(
                    receipt_id=receipt.id,
                    name=item.name,
                    price=item.price,
                    amount=item.amount,
                    assigned_to=user_id,
                )
                for item in items
            )
        return line_items

    @staticmethod
    def _map_to_domain(orm: ReceiptORM) -> Receipt:
        unassigned_items = []
        assignees = defaultdict(list)
        for item_orm in orm.line_items:
            item = LineItem(item_orm.name, item_orm.amount, item_orm.price)
            if item_orm.assigned_to is None:
                unassigned_items.append(item)
            else:
                assignees[UserID(item_orm.assigned_to)].append(item)

        return Receipt(
            id=ReceiptID(orm.id),
            created_at=orm.created_at,
            title=ReceiptTitle(orm.title),
            creditor_id=UserID(orm.creditor_id),
            unassigned_items=unassigned_items,
            assignees=assignees,
        )

    @classmethod
    def _bulk_map_to_domain(
        cls, models: Iterable[ReceiptORM]
    ) -> list[Receipt]:
        return [cls._map_to_domain(model) for model in models]
