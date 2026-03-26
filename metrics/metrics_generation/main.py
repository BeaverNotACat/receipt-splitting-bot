import asyncio
import json
import os
import time
from pathlib import Path
from typing import cast

from pydantic import TypeAdapter

from metrics.metrics_generation.generator import (
    MetricsModelClient,
    TestCreator,
    TestItem,
)
from metrics.metrics_generation.texts import (
    variant_target_meals,
    variant_target_names,
)
from src.presentation.dependencies.container import container

BASE_DIR = Path(__file__).parent
STATE_FILE = BASE_DIR / "data" / "tests.jsonl"
if not STATE_FILE.exists():
    BASE_DIR = Path(__file__).parent
    STATE_FILE.touch()


def append_jsonl(
        path: Path, obj: TestItem, adapter: TypeAdapter[TestItem]
        ) -> None:
    line = adapter.dump_json(obj)

    with path.open("ab") as f:
        f.write(line)

    with path.open("a", encoding="utf-8") as f:
        f.write("\n")
        f.flush()


def load_last_test_id(path: Path) -> int:
    """Возвращает test_id последнего записанного теста,
       или 0, если файл пустой."""
    with path.open("rb") as f:

        f.seek(-2, os.SEEK_END)

        end = f.tell()
        if end == 0:
            return 0

        try:
            while f.read(1) != b"\n":
                f.seek(-2, os.SEEK_CUR)

        except OSError:
            f.seek(0)
        last_line = f.readline().decode()
        return cast(json.loads(last_line)["id"])


def is_rate_limit_error(exc: Exception) -> bool:
    """Временная мера"""
    msg = str(exc).lower()
    return "429" in msg or "rate limit" in msg or "too many requests" in msg


def main() -> None:
    client = asyncio.run(container.get(MetricsModelClient))
    adapter = TypeAdapter(TestItem)

    test_creator = TestCreator(
        variant_target_names=variant_target_names,
        variant_target_meals=variant_target_meals,
        client=client)

    start_id = load_last_test_id(STATE_FILE)

    test_id = start_id
    while True:
        try:
            test = test_creator.generate_test_item(test_id=test_id)
            append_jsonl(STATE_FILE, test, adapter)
            test_id += 1

        except Exception as exc:
            if is_rate_limit_error(exc):
                wait_seconds = 3600
                time.sleep(wait_seconds)
                continue

            raise
