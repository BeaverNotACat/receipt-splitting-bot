import asyncio
from pathlib import Path

from metrics.agent_metrics.metrics_execution.executor import calculate_metrics

BASE_DIR = Path(__file__).resolve().parents[2]
STATE_FILE = BASE_DIR / "data" / "agent_metrics" / "tests.jsonl"
SUMMARY_FILE = BASE_DIR / "data" / "agent_metrics" / "summary.jsonl"
ITEM_METRICS_FILE = BASE_DIR / "data" / "agent_metrics" / "item_metrics.jsonl"


async def main() -> None:
    await calculate_metrics(STATE_FILE, SUMMARY_FILE, ITEM_METRICS_FILE, 10)


if __name__ == "__main__":
    asyncio.run(main())
