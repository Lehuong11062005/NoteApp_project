from pydantic import BaseModel, Field
from typing import Optional

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

class RegisterRequest(BaseModel):
    """Dữ liệu gửi lên khi đăng kí tài khoản mới."""
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=6)
    email: Optional[str] = None
    full_name: Optional[str] = None

class RegisterResponse(BaseModel):
    """Kết quả trả về sau khi đăng kí thành công."""
    message: str
    username: str

class UserProfileResponse(BaseModel):
    """Schema trả về thông tin cá nhân user từ GET /auth/profile"""
    user_id: str
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    avatar_url: Optional[str] = None
    created_at: Optional[str] = None