import uuid
from datetime import UTC, datetime
from decimal import Decimal
from pathlib import Path
from random import choice, randint

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openrouter import ChatOpenRouter
from pydantic.dataclasses import dataclass

from metrics.metrics_generation.texts import PROMPT_TEMPLATE
from src.domain.models import Receipt
from src.domain.models.user import DummyUser, User
from src.domain.value_objects import (
    LineItem,
    ReceiptID,
    ReceiptTitle,
    UserID,
    UserNickname,
)


@dataclass(frozen=True)
class TestItem:
    """Item used for testing receipt-splitting model"""

    id: int
    target: Receipt
    bill: Bill
    user_message: str
    participants: list[User]


@dataclass(frozen=True)
class Bill:
    """Bill that party was given"""

    lines: list[LineItem]


@dataclass(frozen=True)
class Menu:
    """Initial menu of restuarant"""

    positions: list[Position]


@dataclass(frozen=True)
class Position:
    """Menu containment"""

    name: str
    price: int


BASE_DIR = Path(__file__).resolve().parent


class TestCreator:
    def __init__(
        self,
        variant_target_meals: list[str],
        variant_target_names: list[str],
        client: ChatOpenRouter,
        prompt_template: str = PROMPT_TEMPLATE,
    ) -> None:
        self.variant_target_meals = variant_target_meals
        self.variant_target_names = variant_target_names
        self.prompt_template = prompt_template
        self.model = create_agent(client)

    def generate_test_item(self, test_id: int) -> TestItem:
        menu = self._create_menu()
        users = self._create_participants(randint(1, 10))
        target = self._create_target(menu, users)
        users_mapping = self._build_users_mapping(users)
        return TestItem(
            id=test_id,
            target=target,
            bill=self._make_bill(target),
            user_message=self.model.invoke(
                {
                    "messages": [
                        HumanMessage(
                            content=self._target_to_prompt(
                                target, users_mapping
                            )
                        )
                    ]
                }
            )["messages"][-1].content,
            participants=users,
        )

    def _create_menu(self) -> Menu:
        return Menu(
            positions=[
                Position(name=meal, price=randint(100, 1000))
                for meal in self.variant_target_meals
            ]
        )

    def _create_participants(self, users_count: int) -> list[User]:
        users: list[User] = []
        for _ in range(users_count):
            user_name = choice(self.variant_target_names)
            user_id = uuid.uuid4()
            users.append(
                DummyUser(id=UserID(user_id), nickname=UserNickname(user_name))
            )
        return users

    @staticmethod
    def _create_target(menu: Menu, users: list[User]) -> Receipt:
        assignees: dict[UserID, list[LineItem]] = {}
        last_user: UserID

        for user in users:
            meals = [
                LineItem(
                    name=pos.name,
                    amount=Decimal(randint(10, 30) / 10),
                    price=Decimal(pos.price),
                )
                for pos in (
                    choice(menu.positions) for _ in range(randint(1, 5))
                )
            ]
            last_user = user.id
            assignees[user.id] = meals
        return Receipt(
            unassigned_items=[],
            assignees=assignees,
            id=ReceiptID(uuid.uuid4()),
            created_at=datetime.now(UTC),
            title=ReceiptTitle("123"),
            creditor_id=last_user,
        )

    @staticmethod
    def _build_users_mapping(users: list[User]) -> dict[UserID, str]:
        return {user.id: user.nickname for user in users}

    @staticmethod
    def _make_bill(target: Receipt) -> Bill:
        lines: list[LineItem] = []

        all_items = [
            *target.unassigned_items,
            *(item for items in target.assignees.values() for item in items),
        ]

        for item in all_items:
            lines = target._add_to_collection(lines, item)  # noqa: SLF001

        return Bill(lines=lines)

    def _target_to_prompt(
        self, target: Receipt, user_mapping: dict[UserID, str]
    ) -> str:
        lines: list[str] = []

        for i, (user_id, items) in enumerate(
            target.assignees.items(), start=1
        ):
            user_name = user_mapping.get(user_id)
            if items:
                meals_list = ", ".join(item.name for item in items)
            else:
                meals_list = "ничего"

            lines.append(f"{i}. {user_name} ел: {meals_list}")

        return self.prompt_template.format(lines="\n".join(lines))
