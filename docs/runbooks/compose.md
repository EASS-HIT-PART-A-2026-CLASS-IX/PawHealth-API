# Compose Runbook — PawHealth Pro

## Prerequisites
- Docker Desktop running
- Ports 6379, 8000, 8001, 8501 free

## Launch the full stack
```bash
docker compose up -d --build
```

Services start in dependency order: Redis → API → Frontend. The sidecar starts in parallel.

## Verify all services are healthy
```bash
docker compose ps
```
All four containers should show `(healthy)` or `Up`.

## Verify API health and telemetry headers
```bash
curl -i http://localhost:8000/healthz
```
Expected: `200 OK` with `x-trace-id` and `x-request-id` headers.

## Verify Redis is accepting connections
```bash
docker compose exec redis redis-cli ping
```
Expected: `PONG`

## Run the async refresh worker (Session 09)
```bash
uv run python scripts/refresh.py
```
The script connects to Redis, writes idempotency keys, then calls the API concurrently (max 3 in-flight).

## Run the test suite
```bash
uv run pytest tests/ -v
```

## Tear down
```bash
docker compose down
```
