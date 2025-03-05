from pydantic import BaseModel, EmailStr, Field

class UserSignUp(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    product_id: str = "1112"  # Default value as specified

class UserSignIn(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"