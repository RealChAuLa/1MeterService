from pydantic import BaseModel, EmailStr, Field

class UserSignUp(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6)
    product_id: str = Field(..., min_length=4, max_length=50)

class UserSignIn(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class User(BaseModel):
    username: str
    product_id: str