from fastapi import HTTPException, status
from pymongo.database import Database
from pymongo.errors import DuplicateKeyError
from app.schemas.auth_schema import RegisterRequest, RegisterResponse, LoginRequest, TokenResponse
from app.repositories import user_repository
from app.utils.password import get_password_hash, verify_password
from app.middleware.jwt_auth import create_access_token

def register_user(db: Database, request: RegisterRequest) -> RegisterResponse:
    """Xử lý nghiệp vụ đăng ký tài khoản mới"""
    # 1. Kiểm tra username đã tồn tại chưa
    existing_user = user_repository.get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Tên đăng nhập đã tồn tại!"
        )

    # 2. Băm mật khẩu an toàn
    hashed_pw = get_password_hash(request.password)

    # 3. Đóng gói dữ liệu Document
    user_doc = {
        "username": request.username,
        "password": hashed_pw,
        "email": request.email,
        "full_name": request.full_name
    }

    # 4. Lưu vào Database
    try:
        user_repository.create_user(db, user_doc)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Lỗi khi lưu user vào database: {str(e)}"
        )

    return RegisterResponse(
        message="Đăng ký tài khoản thành công!",
        username=request.username
    )

def authenticate_user(db: Database, request: LoginRequest) -> TokenResponse:
    """Xử lý nghiệp vụ đăng nhập và cấp phát JWT token"""
    user = user_repository.get_user_by_username(db, request.username)
    
    # Kiểm tra user tồn tại và so sánh password
    if not user or not verify_password(request.password, user.get("password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu không chính xác!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # MongoDB dùng _id, cần ép kiểu về chuỗi (str)
    user_id = str(user.get("_id"))
    access_token = create_access_token(data={"sub": user.get("username"), "user_id": user_id})
    
    return TokenResponse(
        access_token=access_token,
        token_type="bearer",
        message="Đăng nhập thành công!"
    )