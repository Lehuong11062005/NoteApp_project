from fastapi import HTTPException, status
from app.middleware.jwt_auth import ALGORITHM, SECRET_KEY
from app.repositories.user_repository import UserRepository
from app.schemas.auth_schema import UserRegisterSchema, UserLoginSchema
from app.utils.password import hash_password, verify_password
from datetime import datetime
from typing import Dict, Any
from fastapi import Depends
import jwt
import os
from app.middleware.jwt_auth import create_access_token

class AuthService:
    def __init__(self, user_repo: UserRepository = Depends()):
        self.user_repo = user_repo

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
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, 
                detail="Sai tên đăng nhập hoặc mật khẩu!"
            )
        payload_data = {
            "sub": str(user["_id"]),
            "username": user["username"]
        }
        
        token = create_access_token(data=payload_data)
            
        return {
            "message": "Đăng nhập thành công!",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "id": str(user["_id"]),
                "username": user["username"],
                "fullname": user["fullname"]
            }
        }