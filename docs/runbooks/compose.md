# Deployment Runbook (EX3)

## Local Launch
1. Ensure Docker Desktop is running.
2. Run `docker compose up -d --build`.
3. Verify services are up: `docker compose ps`.

## Health Verification
Run the following to verify the API and Trace ID propagation:
`curl -i http://localhost:8000/healthz`

## Telemetry
The system uses the `x-trace-id` header to track requests across the FastAPI backend and the Streamlit frontend.

## Security
Endpoints under `/dogs/{id}/refresh` require a Bearer token. Unauthorized requests will return a `401`.
