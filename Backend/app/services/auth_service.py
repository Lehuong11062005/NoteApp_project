from fastapi import HTTPException, status
from app.schemas.auth_schema import LoginRequest, TokenResponse
from app.repositories import user_repository
from app.utils.password import verify_password
from app.middleware.jwt_auth import create_access_token

def authenticate_user(db, request: LoginRequest) -> TokenResponse:
    user = user_repository.get_user_by_username(db, request.username)
    
    # Check user tồn tại và so sánh password
    if not user or not verify_password(request.password, user.get("password")):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Tài khoản hoặc mật khẩu không chính xác!",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # MongoDB dùng _id, cần ép kiểu về chuỗi (str)
    user_id = str(user.get("_id"))
    access_token = create_access_token(data={"sub": user.get("username"), "user_id": user_id})
    
    return TokenResponse(access_token=access_token, token_type="bearer")