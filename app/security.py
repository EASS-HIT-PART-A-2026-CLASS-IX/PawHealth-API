import jwt
import bcrypt
from datetime import datetime, timedelta
from fastapi import HTTPException, Header, status
from app.config import settings

# ============= PASSWORD HASHING =============

def hash_password(password: str) -> str:
    """Hash a password using bcrypt."""
    salt = bcrypt.gensalt(rounds=12)
    return bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hash."""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

# ============= JWT CONFIGURATION =============

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# ============= TOKEN GENERATION =============

def create_access_token(data: dict, expires_delta: timedelta = None) -> str:
    """Create a JWT access token.
    
    Args:
        data: Dictionary containing token claims (e.g., {"sub": "user123"})
        expires_delta: Optional custom expiration time
        
    Returns:
        Encoded JWT token string
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret, algorithm=ALGORITHM)
    return encoded_jwt

# ============= TOKEN VALIDATION =============

async def get_current_user(authorization: str = Header(None)) -> dict:
    """Validate Bearer token and extract user information.
    
    Raises:
        HTTPException(401): If token is missing, invalid, or expired
        
    Returns:
        Dictionary with user claims and scope
    """
    if authorization is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Extract token from "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    token = parts[1]
    
    try:
        # Verify token signature and expiration
        payload = jwt.decode(token, settings.jwt_secret, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        scope: str = payload.get("scope", "pet_owner")
        
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token claims",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return {"username": username, "scope": scope}
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
            headers={"WWW-Authenticate": "Bearer"},
        )

