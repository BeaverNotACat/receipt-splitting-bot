import asyncio
from pathlib import Path

from metrics.metrics_execution.executor import calculate_metrics

BASE_DIR = Path(__file__).resolve().parents[1]
STATE_FILE = BASE_DIR / "data" / "tests.jsonl"
SUMMARY_FILE = BASE_DIR / "data" / "summary.jsonl"
ITEM_METRICS_FILE = BASE_DIR / "data" / "item_metrics.jsonl"


async def main() -> None:
    await calculate_metrics(STATE_FILE, SUMMARY_FILE, ITEM_METRICS_FILE, 100)


if __name__ == "__main__":
    asyncio.run(main())
