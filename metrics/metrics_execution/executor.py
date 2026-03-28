import json
from decimal import Decimal
from pathlib import Path

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
class Metrics:
    item_metrics: list[ItemMetrics]
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


test_item_adapter = TypeAdapter(TestItem)


async def calculate_metrics(tests_path: Path, tests_count: int) -> Metrics:  # noqa: PLR0914
    agent = await container.get(AgentI)

    with tests_path.open(encoding="utf-8") as f:
        line_metrics: list[ItemMetrics] = []

        global_absolute_error = 0
        gloabal_samples_count = 0
        global_percentage_error = 0

        global_people_common = 0
        global_people_missing = 0
        global_people_extra = 0

        global_meals_common = 0
        global_meals_missing = 0
        global_meals_extra = 0

        count = 0
        while count < tests_count:
            count += 1
            line = json.loads(f.readline())
            test_item = test_item_adapter.validate_python(line)
            target = test_item.target

            actual = (await agent.invoke(
                request=HumanRequest(
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
                    creditor_id=target.creditor_id
                ),
                participants=test_item.participants
            )).updated_receipt

            target_people = set(target.assignees.keys())
            actual_people = set(actual.assignees.keys())

            people_common = target_people & actual_people
            people_missing = target_people - actual_people
            people_extra = actual_people - target_people

            global_people_common += len(people_common)
            global_people_missing += len(people_missing)
            global_people_extra += len(people_extra)

            absolute_error = 0
            samples = 0
            for name in people_common:
                t_meals = target.assignees[name]
                a_meals = actual.assignees[name]

                t_set = set(t_meals.keys())
                a_set = set(a_meals.keys())

                common_meals = t_set & a_set
                missing_meals = t_set - a_set
                extra_meals = a_set - t_set

                global_meals_common += len(common_meals)
                global_meals_missing += len(missing_meals)
                global_meals_extra += len(extra_meals)

                global_percentage_error += [
                    abs(t_meals[meal].price - a_meals[meal].price)
                    / t_meals.price
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
                    meals_common=len(common_meals),
                    meals_missing=len(missing_meals),
                    meals_extra=len(extra_meals),
                    price_mae=mae,
                )
            people_precision = len(people_common) / len(
                people_common + people_extra
            )
            people_recall = len(people_common) / len(
                people_common + people_missing
            )
            line_metrics.append(
                ItemMetrics(
                    id=test_item.id,
                    price_mae=absolute_error / samples,
                    people_f1=2
                    * (people_precision * people_recall)
                    / (people_precision + people_recall),
                    personal_stats=personal_stats,
                )
            )
    return Metrics(
        item_metrics=line_metrics,
        price_mae=global_absolute_error / gloabal_samples_count,
        price_mpe=global_percentage_error / gloabal_samples_count,
        people_f1=calculate_f1(
            global_people_common, global_people_extra, global_people_missing
            ),
        meals_f1=calculate_f1(
            global_meals_common, global_meals_missing, global_meals_extra
        ),
    )


def calculate_f1(tp: Decimal, fp: Decimal, fn: Decimal) -> Decimal:
    precision = tp / (tp + fn)
    recall = tp / (tp + fp)
    return (2 * precision * recall) / (precision + recall)
