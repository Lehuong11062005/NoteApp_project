from fastapi import APIRouter, Depends
from app.schemas.auth_schema import UserRegisterSchema, UserLoginSchema
from app.services.auth_service import AuthService
from app.middleware.jwt_auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()

@router.post("/register")
def register_user(payload: UserRegisterSchema):
    return auth_service.register(payload)

@router.post("/login")
def login_user(payload: UserLoginSchema):
    return auth_service.login(payload)

@router.get("/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "username": current_user["username"],
        "fullname": current_user["fullname"],
        "email": current_user.get("email", "")
    }