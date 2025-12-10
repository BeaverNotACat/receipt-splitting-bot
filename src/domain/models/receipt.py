from dataclasses import dataclass

from pydantic import AwareDatetime  # noqa: TC002

from src.domain.exceptions import (
    AlreadyParticipantError,
    AssignNotToParticipantError,
    ItemNotInCollectionError,
    NotDebtorError,
    RemovedMoreThanExistError,
)
from src.domain.models.user import User  # noqa: TC001
from src.domain.value_objects import LineItem, ReceiptID, UserID


@dataclass
class Receipt:
    id: ReceiptID
    created_at: AwareDatetime
    title: str

    creditor_id: UserID
    debtors_ids: list[UserID]

    unassigned_items: list[LineItem]
    assignees: dict[UserID, list[LineItem]]

    @property
    def participants_ids(self) -> list[UserID]:
        return [*self.debtors_ids, self.creditor_id]

    def append_item(self, item: LineItem) -> None:
        self.unassigned_items = self._add_to_collection(
            self.unassigned_items, item
        )

    def remove_item(self, item: LineItem) -> None:
        self.unassigned_items = self._remove_from_collection(
            self.unassigned_items, item
        )

    def assign_item(self, item: LineItem, user: User) -> None:
        self._ensure_participant(user)

        self.unassigned_items = self._remove_from_collection(
            self.unassigned_items, item
        )
        self.assignees[user.id] = self._add_to_collection(
            self.assignees.get(user.id, []), item
        )

    def disassign_item(self, item: LineItem, user: User) -> None:
        self._ensure_participant(user)

        self.assignees[user.id] = self._remove_from_collection(
            self.assignees[user.id], item
        )
        self.unassigned_items = self._add_to_collection(
            self.unassigned_items, item
        )

    def append_debtor(self, user: User) -> None:
        if user.id in self.participants_ids:
            raise AlreadyParticipantError
        self.debtors_ids.append(user.id)
        self.assignees[user.id] = []

    def remove_debtor(self, user: User) -> None:
        self._ensure_debtor(user)
        for item in self.assignees[user.id]:
            self.unassigned_items = self._add_to_collection(
                self.unassigned_items, item
            )
        del self.assignees[user.id]
        self.debtors_ids.remove(user.id)

    @staticmethod
    def _remove_from_collection(
        collection: list[LineItem], item: LineItem
    ) -> list[LineItem]:
        if item not in collection:
            raise ItemNotInCollectionError
        collection = collection.copy()

        collection[collection.index(item)], collection[-1] = (
            collection[-1],
            collection[collection.index(item)],
        )
        free_item = collection.pop()

        free_amount = free_item.amount - item.amount
        if free_amount > 0:
            collection.append(LineItem(item.name, free_amount, item.price))
        elif free_amount < 0:
            raise RemovedMoreThanExistError

        return collection

    @staticmethod
    def _add_to_collection(
        collection: list[LineItem], item: LineItem
    ) -> list[LineItem]:
        collection = collection.copy()
        owned_amount = item.amount
        if item in collection:
            collection[collection.index(item)], collection[-1] = (
                collection[-1],
                collection[collection.index(item)],
            )
            owned_item = collection.pop()
            owned_amount += owned_item.amount
        collection.append(LineItem(item.name, owned_amount, item.price))
        return collection

    def _ensure_participant(self, user: User) -> None:
        if user.id not in self.participants_ids:
            raise AssignNotToParticipantError

    def _ensure_debtor(self, user: User) -> None:
        if user.id not in self.debtors_ids:
            raise NotDebtorError
