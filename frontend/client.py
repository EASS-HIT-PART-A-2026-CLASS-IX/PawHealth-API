import httpx

# FastAPI is strict about trailing slashes. 
# Added '/' to avoid 307 Redirect errors.
BASE_URL = "http://127.0.0.1:8000"

def get_dogs():
    try:
        # Using follow_redirects=True as a fail-safe
        response = httpx.get(f"{BASE_URL}/dogs/", timeout=10.0, follow_redirects=True)
        return response.json()
    except Exception:
        return []

def add_dog(name: str, breed: str, age: int):
    payload = {"name": name, "breed": breed, "age": age}
    # Ensure the URL ends with / to match FastAPI router patterns
    response = httpx.post(f"{BASE_URL}/dogs/", json=payload, timeout=10.0, follow_redirects=True)
    response.raise_for_status()
    return response.json()
