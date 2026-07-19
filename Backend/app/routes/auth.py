from fastapi import APIRouter, Depends
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.services import auth_service
from app.config.database import get_database

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(request_data: LoginRequest, db = Depends(get_database)):
    """API Đăng nhập"""
    return auth_service.authenticate_user(db, request_data)