from fastapi import APIRouter
from app.schemas.auth_schema import UserRegisterSchema, UserLoginSchema
from app.services.auth_service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])
auth_service = AuthService()
@router.post("/register")
def register_user(payload: UserRegisterSchema):
    return auth_service.register(payload)

@router.post("/login")
def login_user(payload: UserLoginSchema):
    return auth_service.login(payload)