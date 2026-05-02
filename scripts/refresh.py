import httpx
import asyncio
import uuid

async def refresh_dog_data(dog_id: int):
    # EX3 Requirement: Idempotency & Retries
    url = f"http://localhost:8000/dogs/{dog_id}/refresh"
    headers = {"X-Idempotency-Key": str(uuid.uuid4())}
    
    async with httpx.AsyncClient() as client:
        for attempt in range(3):  # Simple retry logic
            try:
                response = await client.post(url, headers=headers, timeout=5.0)
                return response.status_code
            except httpx.RequestError:
                if attempt == 2: return 500
                await asyncio.sleep(1)

async def main():
    dog_ids = [1, 2, 3, 4, 5]  # Example IDs
    results = await asyncio.gather(*(refresh_dog_data(i) for i in dog_ids))
    print(f"Refresh task completed with results: {results}")

if __name__ == "__main__":
    asyncio.run(main())
