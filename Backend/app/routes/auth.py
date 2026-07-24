from fastapi import APIRouter, Depends, status
from pymongo.database import Database
from app.config.database import get_database
from app.schemas.auth_schema import RegisterRequest, RegisterResponse, LoginRequest, TokenResponse
from app.services import auth_service

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(request_data: RegisterRequest, db: Database = Depends(get_database)):
    """API Đăng ký tài khoản mới"""
    return auth_service.register_user(db, request_data)

@router.post("/login", response_model=TokenResponse)
def login(request_data: LoginRequest, db: Database = Depends(get_database)):
    """API Đăng nhập"""
    return auth_service.authenticate_user(db, request_data)