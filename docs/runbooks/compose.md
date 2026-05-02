# EX3 Runbook - PawHealth Management

## How to Start the Project
To launch all services (API, Redis, Sidecar, and UI) in a single command, run:
\`\`\`bash
docker compose up --build
\`\`\`

## Service Ports
- **FastAPI Backend:** http://localhost:8000
- **AI Sidecar:** http://localhost:8001
- **Streamlit UI:** http://localhost:8501

## Verification
1. **Health Check:** curl http://localhost:8000/healthz
2. **Async Jobs:** Run 'uv run python scripts/refresh.py'
