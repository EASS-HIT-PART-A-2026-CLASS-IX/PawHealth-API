FROM ghcr.io/astral-sh/uv:latest AS uv
FROM python:3.12-slim
RUN apt-get update && apt-get install -y curl && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY --from=uv /uv /bin/uv
COPY . .
RUN uv sync --frozen
CMD ["uv", "run", "uvicorn app.main:app", "--host", "0.0.0.0", "--port", "8000"]
