from fastapi import HTTPException, Header, status

async def get_current_user(authorization: str = Header(None)):
    """
    Validates the Authorization header.
    Raises 401 if the header is missing or invalid.
    """
    if authorization is None or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Mock user for EX3 requirements
    return {"username": "authenticated_user", "scope": "pet_owner"}
