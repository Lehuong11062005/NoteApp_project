from pydantic import BaseModel, Field
from typing import Optional

class RegisterRequest(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)
    email: Optional[str] = None
    full_name: Optional[str] = None

class RegisterResponse(BaseModel):
    message: str
    username: str

class LoginRequest(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    message: str