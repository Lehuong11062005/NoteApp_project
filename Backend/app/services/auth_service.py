from fastapi import HTTPException, status
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError
from app.schemas.auth_schema import RegisterRequest, RegisterResponse
from app.repositories import user_repository
from app.utils.password import get_password_hash

def register_user(db: Database, request: RegisterRequest) -> RegisterResponse:
    try:
        # 1. Kiểm tra username đã tồn tại chưa
        existing_user = user_repository.get_user_by_username(db, request.username)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Tên đăng nhập đã tồn tại!"
            )

        # 2. Băm mật khẩu
        hashed_pw = get_password_hash(request.password)

        # 3. Đóng gói dữ liệu Document
        user_doc = {
            "username": request.username,
            "password": hashed_pw,
            "email": request.email,
            "full_name": request.full_name
        }

        # 4. Lưu vào Database
        user_repository.create_user(db, user_doc)

        return RegisterResponse(
            message="Đăng ký tài khoản thành công!",
            username=request.username
        )
        
    except HTTPException as he:
        # Giữ nguyên các lỗi 409 hoặc lỗi logic đã định nghĩa
        raise he
    except Exception as e:
        # Nếu có lỗi bất ngờ từ MongoDB hoặc hệ thống, in ra terminal Backend và trả về 500 kèm chi tiết
        print(f"LỖI ĐĂNG KÝ CHI TIẾT: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi server: {str(e)}"
        )