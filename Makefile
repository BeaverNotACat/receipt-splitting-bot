format:
	uv run ruff format
	uv run ruff check --fix

lint:
	uv run ruff check
	uv run mypy .

test:
	uv run pytest --cov=src

coverage:
	uv run coverage report -m

make-migrations:
	uv run alchemy --config src.adapters.database.cli_config.config make-migrations

migrate:
	uv run alchemy --config src.adapters.database.cli_config.config upgrade

generate-metrics:
	uv run python -m metrics.metrics_generation.main

execute-metrics:
	uv run python -m metrics.metrics_execution.main

run:
	uv run python -m src.main
