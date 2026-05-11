from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from sqlmodel import Session, select
from app.security import create_access_token, hash_password, verify_password
from app.database import get_session
from app.models import User, UserCreate
from datetime import timedelta

router = APIRouter(tags=["Auth"])

class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

class LoginResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    username: str

@router.post("/register", response_model=LoginResponse)
def register(request: RegisterRequest, session: Session = Depends(get_session)):
    """
    Register a new user account.
    Returns JWT token for immediate use.
    """
    if not request.username or len(request.username.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is required"
        )
    if not request.password or len(request.password) < 6:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password must be at least 6 characters"
        )
    
    # Check if user already exists
    statement = select(User).where(User.username == request.username)
    existing_user = session.exec(statement).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already taken"
        )
    
    # Create new user
    hashed_pwd = hash_password(request.password)
    user = User(username=request.username, hashed_password=hashed_pwd)
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Generate token with 24-hour expiration
    token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "scope": "pet_owner"},
        expires_delta=timedelta(hours=24)
    )
    
    return LoginResponse(access_token=token, username=user.username)

@router.post("/login", response_model=LoginResponse)
def login(request: LoginRequest, session: Session = Depends(get_session)):
    """
    Login with username and password.
    Returns JWT token for authenticated requests.
    """
    if not request.username or len(request.username.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username is required"
        )
    if not request.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Password is required"
        )
    
    # Find user by username
    statement = select(User).where(User.username == request.username)
    user = session.exec(statement).first()
    
    if not user or not verify_password(request.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password"
        )
    
    # Generate token with 24-hour expiration
    token = create_access_token(
        data={"sub": user.username, "user_id": user.id, "scope": "pet_owner"},
        expires_delta=timedelta(hours=24)
    )
    
    return LoginResponse(access_token=token, username=user.username)
