FROM ghcr.io/astral-sh/uv:alpine

WORKDIR /receipt-splitting-bot

COPY pyproject.toml uv.lock .python-version .
RUN	uv sync --frozen

COPY . .

CMD [ "uv", "run", "python", "-m", "src.main" ]
