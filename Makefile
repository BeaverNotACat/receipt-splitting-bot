format:
	uv run ruff format
	uv run ruff check --fix

lint:
	uv run ruff check
	uv run mypy .

test:
	uv run pytest

make-migrations:
	uv run alchemy --config src.adapters.database.cli_config.config make-migrations

migrate:
	uv run alchemy --config src.adapters.database.cli_config.config upgrade
