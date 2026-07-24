from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional

class RegisterRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    username: str = Field(
        ..., 
        min_length=3, 
        max_length=50, 
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Chỉ chứa chữ cái không dấu, số, gạch dưới và gạch ngang"
    )
    password: str = Field(
        ..., 
        min_length=8,  
        max_length=128, 
        description="Mật khẩu tối thiểu 8 ký tự và tối đa 128 ký tự"
    )
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=100)

class RegisterResponse(BaseModel):
    message: str
    username: str

class LoginRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8, max_length=128)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer", pattern="(?i)^bearer$") 
    message: str