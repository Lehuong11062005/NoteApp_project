from fastapi import HTTPException, status
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import UserRegisterSchema, UserLoginSchema
from app.utils.password import hash_password, verify_password
from datetime import datetime, timedelta
from typing import Dict, Any
from jose import jwt
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))


def create_access_token(data: dict) -> str:
    """Tạo JWT access token từ payload data."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register(self, user_data: UserRegisterSchema) -> Dict[str, Any]:
        if self.user_repo.find_by_username(user_data.username):
            raise HTTPException(status_code=400, detail="Tên đăng nhập đã tồn tại!")

        if self.user_repo.find_by_email(user_data.email):
            raise HTTPException(status_code=400, detail="Email này đã được sử dụng!")

        hashed_pwd = hash_password(user_data.password)
        new_user = {
            "username": user_data.username,
            "password": hashed_pwd,
            "fullname": user_data.fullname,
            "email": user_data.email,
            "created_at": datetime.now()
        }

        user_id = self.user_repo.create_user(new_user)
        return {"message": "Đăng ký thành công!", "user_id": user_id}

    def login(self, user_data: UserLoginSchema) -> Dict[str, Any]:
        user = self.user_repo.find_by_username(user_data.username)
        if not user or not verify_password(user_data.password, user["password"]):
            raise HTTPException(status_code=401, detail="Sai tên đăng nhập hoặc mật khẩu!")

        # Tạo JWT token với payload chứa username
        token = create_access_token(data={"sub": user["username"]})

        return {
            "message": "Đăng nhập thành công!",
            "token": token,
            "user": {
                "username": user["username"],
                "fullname": user["fullname"]
            }
        }