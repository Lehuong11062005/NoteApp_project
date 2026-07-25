from pydantic import BaseModel, Field, EmailStr, ConfigDict, field_validator
from typing import Optional

class RegisterRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    username: str = Field(
        ..., 
        pattern=r"^[a-zA-Z0-9_-]+$",
        description="Chỉ chứa chữ cái không dấu, số, gạch dưới và gạch ngang"
    )
    password: str = Field(
        ..., 
        description="Mật khẩu tối thiểu 8 ký tự và tối đa 128 ký tự"
    )
    email: Optional[EmailStr] = Field(default=None, max_length=255)
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=100)

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str) -> str:
        if not value or len(value.strip()) < 3:
            raise ValueError("Tên đăng nhập phải có ít nhất 3 ký tự bạn nhé.")
        if len(value.strip()) > 50:
            raise ValueError("Tên đăng nhập không được vượt quá 50 ký tự.")
        return value

    @field_validator("password")
    @classmethod
    def validate_password(cls, value: str) -> str:
        if not value or len(value) < 8:
            raise ValueError("Mật khẩu quá ngắn, vui lòng nhập tối thiểu từ 8 ký tự trở lên.")
        if len(value) > 128:
            raise ValueError("Mật khẩu quá dài, tối đa là 128 ký tự.")
        return value

class RegisterResponse(BaseModel):
    message: str
    username: str

class LoginRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    username: str = Field(...)
    password: str = Field(...)

    @field_validator("username")
    @classmethod
    def validate_login_username(cls, value: str) -> str:
        if not value or len(value.strip()) < 3:
            raise ValueError("Tên đăng nhập không được để trống hoặc quá ngắn.")
        return value

    @field_validator("password")
    @classmethod
    def validate_login_password(cls, value: str) -> str:
        if not value or len(value) < 8:
            raise ValueError("Mật khẩu đăng nhập cần phải có từ 8 ký tự trở lên.")
        return value

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = Field(default="bearer", pattern="(?i)^bearer$") 
    message: str