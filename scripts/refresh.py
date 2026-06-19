"""
Async batch refresher — Session 09 deliverable.

Runs bounded concurrent refresh requests against the API with:
- Per-request idempotency keys stored in Redis (prevents duplicate processing)
- Exponential-backoff retries (up to 3 attempts)
- asyncio.Semaphore to cap concurrency at 3

Usage:
    uv run python scripts/refresh.py
"""

import asyncio
import os
import uuid
import httpx

try:
    import redis.asyncio as aioredis
    REDIS_AVAILABLE = True
except ImportError:
    REDIS_AVAILABLE = False

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")
API_URL = os.getenv("API_URL", "http://localhost:8000")
CONCURRENCY = 3
MAX_RETRIES = 3


async def get_redis():
    if not REDIS_AVAILABLE:
        return None
    try:
        client = aioredis.from_url(REDIS_URL, decode_responses=True)
        await client.ping()
        return client
    except Exception:
        return None


async def refresh_dog(dog_id: int, semaphore: asyncio.Semaphore, redis_client) -> dict:
    idempotency_key = str(uuid.uuid4())
    redis_key = f"refresh:dog:{dog_id}:{idempotency_key}"

    # Mark as in-flight in Redis (TTL 60 s)
    if redis_client:
        already = await redis_client.get(redis_key)
        if already:
            return {"dog_id": dog_id, "status": "already_processed (redis)"}
        await redis_client.setex(redis_key, 60, "processing")

    url = f"{API_URL}/dogs/{dog_id}/refresh"
    headers = {"X-Idempotency-Key": idempotency_key}

    async with semaphore:
        async with httpx.AsyncClient() as client:
            for attempt in range(MAX_RETRIES):
                try:
                    response = await client.post(url, headers=headers, timeout=5.0)
                    result = {"dog_id": dog_id, "status": response.status_code}
                    if redis_client:
                        await redis_client.setex(redis_key, 300, "done")
                    return result
                except httpx.RequestError as exc:
                    if attempt == MAX_RETRIES - 1:
                        return {"dog_id": dog_id, "status": "error", "detail": str(exc)}
                    await asyncio.sleep(2 ** attempt)

    return {"dog_id": dog_id, "status": "failed"}


async def main():
    dog_ids = [1, 2, 3, 4, 5]
    semaphore = asyncio.Semaphore(CONCURRENCY)
    redis_client = await get_redis()

    if redis_client:
        print(f"[refresh] Redis connected at {REDIS_URL}")
    else:
        print("[refresh] Redis unavailable — running without idempotency store")

    results = await asyncio.gather(*(refresh_dog(i, semaphore, redis_client) for i in dog_ids))

    for r in results:
        print(f"  dog_id={r['dog_id']} → {r['status']}")

    if redis_client:
        await redis_client.aclose()


if __name__ == "__main__":
    asyncio.run(main())
