import asyncio
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential

# EX3 Requirement: Retries with exponential backoff
@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
async def refresh_dog_data(dog_id: int):
    async with httpx.AsyncClient() as client:
        # EX3 Requirement: Trace-Id and Idempotency
        headers = {
            "X-Trace-Id": f"job-{dog_id}",
            "Idempotency-Key": f"ref-{dog_id}"
        }
        # Assuming the API runs on port 8000
        response = await client.post(f"http://localhost:8000/dogs/{dog_id}/refresh", headers=headers)
        return response.status_code

async def main():
    # EX3 Requirement: Bounded concurrency using Semaphore
    sem = asyncio.Semaphore(3)
    async def bounded_job(i):
        async with sem:
            return await refresh_dog_data(i)

    tasks = [bounded_job(i) for i in range(1, 6)]
    results = await asyncio.gather(*tasks)
    print(f"Refresh task completed with results: {results}")

if __name__ == "__main__":
    asyncio.run(main())
