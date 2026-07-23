from fastapi import APIRouter, HTTPException, status
import bcrypt
from app.schemas.auth_schema import RegisterRequest
# Import trực tiếp biến db từ file database vừa sửa ở trên
from app.config.database import db 

router = APIRouter(tags=["Authentication"])

@router.post("/register")
async def register(user_data: RegisterRequest):
    # 1. Chọn bảng (collection) tên là 'users' trong MongoDB
    users_collection = db["users"]
    
    # 2. Kiểm tra xem username đã tồn tại chưa
    existing_user = await users_collection.find_one({"username": user_data.username})
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tài khoản đã tồn tại!"
        )
    
    # 3. Mã hóa mật khẩu bằng bcrypt
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(user_data.password.encode('utf-8'), salt)
    
    # 4. Chuẩn bị dữ liệu để chèn vào MongoDB
    new_user = {
        "username": user_data.username,
        "password": hashed_password.decode('utf-8') 
    }
    
    # 5. Lưu vào database
    await users_collection.insert_one(new_user)
    
    return {"message": "Đăng ký tài khoản thành công!"}