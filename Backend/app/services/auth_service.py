from fastapi import HTTPException, status
from app.schemas.auth_schema import LoginRequest, TokenResponse, UserProfileResponse, RegisterRequest, RegisterResponse
from app.repositories import user_repository
from app.utils.password import verify_password, get_password_hash
from app.middleware.jwt_auth import create_access_token
from app.models.user import create_user_document

def authenticate_user(db, request: LoginRequest) -> TokenResponse:
    user = user_repository.get_user_by_username(db, request.username)
    
    if not user or not verify_password(request.password, user.get("password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu không chính xác!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = str(user.get("_id"))
    access_token = create_access_token(data={"sub": user.get("username"), "user_id": user_id})
    
    return TokenResponse(access_token=access_token, token_type="bearer")

def get_profile(db, current_user: dict) -> UserProfileResponse:
    """Lấy thông tin cá nhân user đang đăng nhập dựa vào token."""
    user = user_repository.get_user_by_id(db, current_user["user_id"])
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Không tìm thấy thông tin người dùng!"
        )
    
    created_at = user.get("created_at")
    if created_at and hasattr(created_at, "isoformat"):
        created_at = created_at.isoformat()
    elif created_at:
        created_at = str(created_at)
    
    return UserProfileResponse(
        user_id=str(user.get("_id")),
        username=user.get("username", ""),
        email=user.get("email"),
        full_name=user.get("full_name"),
        avatar_url=user.get("avatar_url"),
        created_at=created_at
    )

def register_user(db, request: RegisterRequest) -> RegisterResponse:
    """Xử lý đăng kí tài khoản mới."""
    existing_user = user_repository.get_user_by_username(db, request.username)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tên đăng nhập '{request.username}' đã tồn tại!"
        )

    hashed_pw = get_password_hash(request.password)

    user_doc = create_user_document(
        username=request.username,
        hashed_password=hashed_pw,
        email=request.email,
        full_name=request.full_name
    )

    user_repository.create_user(db, user_doc)

    return RegisterResponse(
        message="Đăng kí tài khoản thành công!",
        username=request.username
    )
