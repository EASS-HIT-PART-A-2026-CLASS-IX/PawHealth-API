FROM ghcr.io/astral-sh/uv:latest AS uv
FROM python:3.12-slim
WORKDIR /app
ENV UV_COMPILE_BYTECODE=1
COPY --from=uv /uv /bin/uv
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
COPY pyproject.toml .
RUN uv sync --no-dev
COPY . .
CMD ["uv", "run", "python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
