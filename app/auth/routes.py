from fastapi import APIRouter, Depends, status
from app.auth.models import UserSignUp, UserSignIn, TokenResponse, User
from app.auth.service import AuthService

router = APIRouter()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserSignUp):
    """
    Register a new user
    - Creates a new user in the Firebase Realtime Database
    - Hashes the password for secure storage
    """
    return AuthService.signup(user_data)

@router.post("/signin", response_model=User)
async def login_user(user_data: UserSignIn):
    """
    Authenticate a user
    - Verifies username and password
    - Returns a JWT token for authenticated API access
    - Returns the user's product_id
    """
    return AuthService.signin(user_data)