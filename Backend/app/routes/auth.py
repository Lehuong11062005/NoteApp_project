from fastapi import APIRouter, Depends
from app.schemas.auth_schema import LoginRequest, TokenResponse, UserProfileResponse, RegisterRequest, RegisterResponse
from app.services import auth_service
from app.config.database import get_database
from app.middleware.jwt_auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
def login(request_data: LoginRequest, db = Depends(get_database)):
    """API Đăng nhập"""
    return auth_service.authenticate_user(db, request_data)

@router.post("/register", response_model=RegisterResponse, status_code=201)
def register(request_data: RegisterRequest, db = Depends(get_database)):
    """API Đăng ký tài khoản mới"""
    return auth_service.register_user(db, request_data)

@router.get("/profile", response_model=UserProfileResponse)
def get_profile(
    current_user: dict = Depends(get_current_user),
    db = Depends(get_database)
):
    """API GET /profile lấy thông tin user đang đăng nhập (Bearer token)"""
    return auth_service.get_profile(db, current_user)
