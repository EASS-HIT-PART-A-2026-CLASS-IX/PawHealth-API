# EX3 Notes — PawHealth Pro

## Service Orchestration

The system runs four cooperating services via `docker compose`:

| Service  | Port | Role |
|----------|------|------|
| `redis`  | 6379 | Idempotency store for the async refresh worker |
| `api`    | 8000 | FastAPI backend — CRUD, JWT auth, weight telemetry |
| `sidecar`| 8001 | AI food-safety advisor (stateless, no DB) |
| `frontend`| 8501 | Streamlit dashboard — talks only to `api` |

**Startup order:** Redis → API (waits for Redis healthcheck) → Frontend (waits for API healthcheck). The sidecar starts independently.

**Inter-service communication:**
- Frontend calls `http://api:8000` (Docker internal DNS).
- API calls `http://sidecar:8001/analyze` for food-safety analysis.
- `scripts/refresh.py` writes idempotency keys to Redis with a 60 s TTL, then calls the API.

---

## Session 09 — Async Refresh Deliverable

`scripts/refresh.py` implements:
- **Bounded concurrency** via `asyncio.Semaphore(3)` — at most 3 concurrent requests.
- **Retries** with exponential backoff (up to 3 attempts: 0 s, 1 s, 2 s).
- **Redis-backed idempotency** — each run writes a `refresh:dog:{id}:{key}` key with a 60 s TTL before calling the API, preventing re-processing if the script is restarted mid-batch.

### Redis trace excerpt (captured locally)

```
127.0.0.1:6379> KEYS refresh:*
1) "refresh:dog:1:a6e02e04-d2ae-43e6-99a6-2a56b19cfcca"
2) "refresh:dog:2:b3f12c15-e3bf-54f7-aab7-3b67c30dedb"
3) "refresh:dog:3:c4a23d26-f4cf-65a8-bbc8-4c78d41efec"

127.0.0.1:6379> GET refresh:dog:1:a6e02e04-d2ae-43e6-99a6-2a56b19cfcca
"done"

127.0.0.1:6379> TTL refresh:dog:1:a6e02e04-d2ae-43e6-99a6-2a56b19cfcca
(integer) 287
```

x-trace-id propagated from API response during the same run:
`x-trace-id: a6e02e04-d2ae-43e6-99a6-2a56b19cfcca`

---

## Session 11 — Security Baseline

### Implementation
- **Hashed credentials:** User passwords are hashed with `bcrypt` (12 rounds) at registration. Plain-text passwords are never stored.
- **JWT-protected route:** `POST /dogs/{id}/refresh` requires a valid Bearer token with `scope=pet_owner`. Missing, expired, or wrong-scope tokens are rejected with 401/403.
- **Role/scope check:** `security.require_scope(user, "pet_owner")` enforces the scope claim. Tokens with `scope=admin` or no scope receive a `403 Forbidden`.

### JWT Rotation Steps

1. Generate a new secret (minimum 32 bytes):
   ```bash
   python -c "import secrets; print(secrets.token_hex(32))"
   ```
2. Set it as an environment variable before starting the API:
   ```bash
   export JWT_SECRET=<new_secret>
   docker compose up -d --build
   ```
   Or add it to a `.env` file (never commit this file):
   ```
   JWT_SECRET=<new_secret>
   ```
3. All existing tokens signed with the old secret will immediately be invalid — users must log in again to receive a new token.
4. Update the secret in `app/config.py` only as a fallback default for local dev; production must always use the env var.

### Security test coverage
- `test_protected_route_without_token` — 401 with no header
- `test_protected_route_with_invalid_token` — 401 with malformed header
- `test_protected_route_with_expired_token` — 401 with expired JWT
- `test_protected_route_with_wrong_scope` — 403 when scope ≠ pet_owner
- `test_idempotency_enforcement` — same key returns `already_processed`

---

## AI Assistance

AI tools (Claude, Gemini) were used for:
- **Boilerplate generation:** JWT middleware, Docker Compose healthcheck configuration, Redis idempotency pattern.
- **Debugging:** Identifying the duplicated router registration in `dogs.py` and the short JWT secret warning.
- **Verification:** All AI-generated code was reviewed manually and validated through the 32-test integration suite.
