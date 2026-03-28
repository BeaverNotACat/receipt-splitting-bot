import asyncio
from pathlib import Path

from metrics.metrics_execution.executor import calculate_metrics

BASE_DIR = Path(__file__).parent
STATE_FILE = BASE_DIR / "metrics" / "metrics_generation" / "data" / "tests.jsonl"

print(asyncio.run(calculate_metrics(STATE_FILE, 1)))
