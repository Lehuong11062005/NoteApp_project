from fastapi import HTTPException, status
from Backend.app.middleware.jwt_auth import ALGORITHM, SECRET_KEY
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import UserRegisterSchema, UserLoginSchema
from app.utils.password import hash_password, verify_password
from datetime import datetime, timedelta
from typing import Dict, Any
import os
import jwt

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
        
        payload = {
        "sub": user["username"],
        "exp": datetime.utcnow() + timedelta(hours=24),
    }

        # 2. Sinh chuỗi JWT Token từ khóa bí mật "321cba"
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
            
        return {
            "message": "Đăng nhập thành công!",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "username": user["username"],
                "fullname": user["fullname"]
            }
        }