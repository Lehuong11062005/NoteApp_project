from fastapi import APIRouter, Depends
from app.middleware.jwt_auth import get_current_user 

router = APIRouter(prefix="/auth", tags=["Auth"])



# Route Lấy thông tin tài khoản 
@router.get("/profile")
def get_profile(current_user: dict = Depends(get_current_user)):
    return {
        "status": "success",
        "data": current_user
    }