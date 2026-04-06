import json
from decimal import Decimal
from pathlib import Path
from typing import Literal

from pydantic import TypeAdapter
from pydantic.dataclasses import dataclass

from metrics.metrics_generation.generator import TestItem
from src.application.common.agent import AgentI, HumanRequest
from src.domain.models.receipt import Receipt
from src.domain.value_objects import (
    MessageText,
    UserID,
)
from src.presentation.dependencies.container import container


@dataclass
class MetricsSummary:
    price_mae: Decimal
    price_mpe: Decimal
    people_f1: Decimal
    meals_f1: Decimal


@dataclass
class ItemMetrics:
    id: Decimal
    price_mae: Decimal
    people_f1: Decimal
    meals_f1: Decimal
    personal_stats: PersonalStats


@dataclass
class PersonalStats:
    id: UserID
    meals_total_target: Decimal
    meals_common: Decimal
    meals_missing: Decimal
    meals_extra: Decimal
    price_mae: Decimal


TestCount = int | Literal["all"]

test_item_adapter = TypeAdapter(TestItem)
summary_adapter = TypeAdapter(MetricsSummary)
item_metrics_adapter = TypeAdapter(ItemMetrics)


async def calculate_metrics(  # noqa: PLR0914, PLR0915
    tests_path: Path,
    summary_out_path: Path,
    item_metrics_path: Path,
    tests_count: TestCount = "all",
) -> None:
    agent = await container.get(AgentI)

    with tests_path.open(encoding="utf-8") as f:
        global_absolute_error = 0
        gloabal_samples_count = 0.00000001
        global_percentage_error = 0

        global_people_common = 0
        global_people_missing = 0
        global_people_extra = 0

        global_meals_common = 0
        global_meals_missing = 0
        global_meals_extra = 0

        count = 0
        while True:
            if tests_count != "all" and count >= tests_count:
                break

            raw_line = f.readline()
            if not raw_line:
                break

            count += 1

            line = json.loads(raw_line)
            test_item = test_item_adapter.validate_python(line)
            target = test_item.target

            actual = (
                await agent.invoke(
                    request=HumanRequest(
                        user_id=target.creditor_id,
                        users_input=MessageText(test_item.user_message),
                        transcribed_photos=[str(test_item.bill)],
                        transcribed_audios=[],
                    ),
                    receipt=Receipt(
                        unassigned_items=[],
                        assignees={},
                        id=target.id,
                        created_at=target.created_at,
                        title=target.title,
                        creditor_id=target.creditor_id,
                    ),
                    participants=test_item.participants,
                )
            ).updated_receipt

            if not actual.participants_ids:
                target_people = set(target.participants_ids)

                global_people_missing += len(target_people)

                for person in target_people:
                    meals = target.assignees[person]
                    global_meals_missing += len(meals)

                continue

            target_people = set(target.participants_ids)
            actual_people = set(actual.participants_ids)

            people_common, people_missing, people_extra = compare_set(
                target_people, actual_people
            )

            global_people_common += len(people_common)
            global_people_missing += len(people_missing)
            global_people_extra += len(people_extra)

            absolute_error = 0
            samples = 0
            for name in people_common:
                t_meals = target.assignees[name]
                a_meals = actual.assignees[name]

                t_set = set(t_meals)
                a_set = set(a_meals)

                common_meals, missing_meals, extra_meals = compare_set(
                    t_set, a_set
                )

                global_meals_common += len(common_meals)
                global_meals_missing += len(missing_meals)
                global_meals_extra += len(extra_meals)

                global_percentage_error += [
                    abs(t_meals[meal].price - a_meals[meal].price)
                    / [item.price for item in t_meals]
                    for meal in common_meals
                ]
                global_absolute_error += [
                    abs(t_meals[meal].price - a_meals[meal].price)
                    for meal in common_meals
                ]
                absolute_error += [
                    abs(t_meals[meal].price - a_meals[meal].price)
                    for meal in common_meals
                ]
                samples += len(common_meals)
                gloabal_samples_count += len(common_meals)
                mae = sum(
                    abs(t_meals[meal] - a_meals[meal]) / len(common_meals)
                    for meal in common_meals
                )

                personal_stats = PersonalStats(
                    id=name,
                    meals_total_target=len(t_set),
                    meals_missing=len(missing_meals),
                    meals_extra=len(extra_meals),
                    price_mae=mae,
                )
            item_metrics = ItemMetrics(
                id=test_item.id,
                price_mae=absolute_error / samples,
                people_f1=calculate_f1(
                    people_common, people_extra, people_missing
                ),
                personal_stats=personal_stats,
            )
            with item_metrics_path.open("ab"):
                f.write(item_metrics_adapter.dump_json(item_metrics))

    metrics = MetricsSummary(
        price_mae=global_absolute_error / gloabal_samples_count,
        price_mpe=global_percentage_error / gloabal_samples_count,
        people_f1=calculate_f1(
            global_people_common, global_people_extra, global_people_missing
        ),
        meals_f1=calculate_f1(
            global_meals_common, global_meals_missing, global_meals_extra
        ),
    )
    with summary_out_path.open("wb") as f:
        f.write(summary_adapter.dump_json(metrics))


def compare_set(a: set, b: set) -> list[set]:
    sets_common = a & b
    sets_missing = a - b
    sets_extra = b - a
    return sets_common, sets_missing, sets_extra


def calculate_f1(tp: float, fp: float, fn: float) -> float:
    if tp == 0:
        return 0
    precision = tp / (tp + fn)
    recall = tp / (tp + fp)
    return (2 * precision * recall) / (precision + recall)
