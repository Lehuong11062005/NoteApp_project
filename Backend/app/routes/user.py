from fastapi import APIRouter, Depends, HTTPException, status
from app.repositories.user_repository import UserRepository
from app.middleware.jwt_auth import verify_token

router = APIRouter(prefix="/user", tags=["User"])

@router.get("/profile")
def get_inf_user(
    current_user: dict = Depends(verify_token), 
    user_repo: UserRepository = Depends()       
):
    username = current_user.get("username")
    
    user_info = user_repo.find_by_username(username)
    
    if not user_info:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Không tìm thấy thông tin người dùng"
        )
        
    # Ép kiểu ObjectId của MongoDB thành Chuỗi (String)
    if "_id" in user_info:
        user_info["_id"] = str(user_info["_id"])
        
    # (Tùy chọn) Xóa mật khẩu bị băm (hashed password) trước khi gửi về Frontend cho an toàn
    if "password" in user_info:
        del user_info["password"]
        
    return user_info
