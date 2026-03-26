import uuid
from decimal import Decimal
from pathlib import Path
from random import choice, randint
from typing import NewType

from langchain.agents import create_agent
from langchain_core.messages import HumanMessage
from langchain_openrouter import ChatOpenRouter
from pydantic.dataclasses import dataclass

from metrics.metrics_generation.texts import prompt_template
from src.domain.models import ReceiptItemsData
from src.domain.models.user import DummyUser, User
from src.domain.value_objects import LineItem, UserID, UserNickname

MetricsModelClient = NewType("MetricsModelClient", ChatOpenRouter)


@dataclass(frozen=True)
class TestItem:
    """Item used for testing receipt-splitting model"""
    id: int
    target: ReceiptItemsData
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
            client: MetricsModelClient,
            prompt_template: str = prompt_template,
            ) -> None:
        self.variant_target_meals = variant_target_meals
        self.variant_target_names = variant_target_names
        self.prompt_template = prompt_template
        self.model = create_agent(client)

    def _create_menu(self) -> Menu:
        return Menu(
            positions=[
                Position(name=meal, price=randint(100, 1000))
                for meal in self.variant_target_meals
            ]
        )

    @staticmethod
    def _create_target(menu: Menu, users: list[User]) -> ReceiptItemsData:
        assignees: dict[UserID, list[LineItem]] = {}
        for user in users:
            meals = [
                    LineItem(
                        name=pos.name,
                        amount=Decimal(randint(1, 3)),
                        price=Decimal(pos.price))
                    for pos in (
                        choice(menu.positions)
                        for _ in range(randint(1, 5))
                    )]
            assignees[user.id] = meals
        return ReceiptItemsData(unassigned_items=[], assignees=assignees)

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
    def _make_bill(target: ReceiptItemsData) -> Bill:
        lines: list[LineItem] = []

        all_items = [
            *target.unassigned_items,
            *(item for items in target.assignees.values() for item in items),
        ]

        for item in all_items:
            lines = target._add_to_collection(lines, item)  # noqa: SLF001

        return Bill(lines=lines)

    @staticmethod
    def _build_users_mapping(users: list[User]) -> dict[UserID, str]:
        return {user.id: user.nickname for user in users}

    def _target_to_prompt(
            self,
            target: ReceiptItemsData,
            user_mapping: dict[UserID, str]
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
                {"messages":
                    [HumanMessage(
                        content=self._target_to_prompt(target, users_mapping)
                        )]
                    }
                )["messages"][-1].content,
            participants=users
        )
