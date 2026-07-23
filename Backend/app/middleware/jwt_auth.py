import os
import jwt
from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from dotenv import load_dotenv

# Tải biến môi trường từ .env
load_dotenv()

SECRET_KEY = os.getenv("JWT_SECRET", "abc123")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Khởi tạo HTTPBearer để lấy Token từ Header "Authorization: Bearer <token>"
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    """
    Dependency kiểm tra JWT Token.
    Áp dụng cho các Route cần bảo mật.
    """
    token = credentials.credentials
    
    try:
        # Giải mã và kiểm tra Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        
        user_id: str = payload.get("sub") or payload.get("user_id")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token không chứa thông tin định danh người dùng.",
                headers={"WWW-Authenticate": "Bearer"},
            )
            
        return payload

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token đã hết hạn. Vui lòng đăng nhập lại.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ hoặc đã bị thay đổi.",
            headers={"WWW-Authenticate": "Bearer"},
        )

# Ví dụ cách dùng tại các Router của Backend (như backend/app/routes/notes.py):
# @router.get("/notes")
# def get_notes(current_user: dict = Depends(get_current_user)):
#     return {"message": "Thành công", "user": current_user}