from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth_schema import UserRegisterSchema, UserLoginSchema
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    user_data: UserRegisterSchema, 
    auth_service: AuthService = Depends() 
):
    """Đăng ký tài khoản mới."""
    return auth_service.register(user_data)


@router.post("/login", status_code=status.HTTP_200_OK)
def login(
    user_data: UserLoginSchema, 
    auth_service: AuthService = Depends() 
):
    """Đăng nhập hệ thống."""
    return auth_service.login(user_data)