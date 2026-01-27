from typing import TYPE_CHECKING

from advanced_alchemy.base import UUIDAuditBase, orm_registry
from sqlalchemy import BIGINT, Column, ForeignKey, Numeric, Table
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from decimal import Decimal
    from uuid import UUID

assignments = Table(
    "debtors",
    orm_registry.metadata,
    Column("users_id", ForeignKey("users.id"), primary_key=True),
    Column("receipts_id", ForeignKey("receipts.id"), primary_key=True),
)


class UserORM(UUIDAuditBase):
    """Both dummy and real users table"""

    __tablename__ = "users"

    nickname: Mapped[str]
    chat_id: Mapped[int | None] = mapped_column(BIGINT, nullable=True)


class ReceiptORM(UUIDAuditBase):
    __tablename__ = "receipts"

    title: Mapped[str]
    creditor_id: Mapped[UUID] = mapped_column(ForeignKey(UserORM.id))
    debtors: Mapped[list[UserORM]] = relationship(
        secondary="debtors", back_populates="receipts", lazy="selectin"
    )
    line_items: Mapped[list[LineItemORM]] = relationship(
        lazy="joined", cascade="all, delete-orphan"
    )


class LineItemORM(UUIDAuditBase):
    __tablename__ = "line_items"

    receipt_id: Mapped[UUID] = mapped_column(ForeignKey(ReceiptORM.id))
    name: Mapped[str]
    price: Mapped[Decimal] = mapped_column(Numeric(2, 8))
    amount: Mapped[Decimal] = mapped_column(Numeric(2, 8))
    assigned_to: Mapped[UUID | None] = mapped_column(ForeignKey(UserORM.id))
