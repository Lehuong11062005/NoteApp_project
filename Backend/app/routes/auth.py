from fastapi import APIRouter, Depends
from pymongo.database import Database
from app.schemas.auth_schema import RegisterRequest, RegisterResponse
from app.services import auth_service
from app.config.database import get_database

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=RegisterResponse, status_code=201)
def register(request_data: RegisterRequest, db: Database = Depends(get_database)):
    """API Đăng ký tài khoản mới"""
    return auth_service.register_user(db, request_data)