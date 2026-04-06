import json
import logging
import os
import time
from pathlib import Path
from typing import cast

from pydantic import TypeAdapter

from metrics.metrics_generation.generator import (
    TestCreator,
    TestItem,
)
from metrics.metrics_generation.model_provider import client
from metrics.metrics_generation.texts import (
    VARIANT_TARGET_MEALS,
    VARIANT_TARGET_NAMES,
)

logger = logging.getLogger(__name__)


BASE_DIR = Path(__file__).resolve().parents[1]
STATE_FILE = BASE_DIR / "data" / "tests.jsonl"
if not STATE_FILE.exists():
    BASE_DIR = Path(__file__).parent
    STATE_FILE.touch()


def append_jsonl(
    path: Path, obj: TestItem, adapter: TypeAdapter[TestItem]
) -> None:
    line = adapter.dump_json(obj).decode("utf-8")

    with path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")


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
        return cast(int, json.loads(last_line)["id"])


def main() -> None:
    test_item_adapter = TypeAdapter(TestItem)

    test_creator = TestCreator(
        variant_target_names=VARIANT_TARGET_NAMES,
        variant_target_meals=VARIANT_TARGET_MEALS,
        client=client,
    )

    test_id = load_last_test_id(STATE_FILE)

    while True:
        try:
            test_id += 1
            test = test_creator.generate_test_item(test_id=test_id)
            append_jsonl(STATE_FILE, test, test_item_adapter)

        except Exception as exc:  # noqa: BLE001
            logger.warning(exc)
            wait_seconds = 3600
            time.sleep(wait_seconds)
            continue


if __name__ == "__main__":
    main()
