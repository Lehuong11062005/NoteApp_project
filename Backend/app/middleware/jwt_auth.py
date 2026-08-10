import os
import jwt
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv

load_dotenv()

# Lấy cấu hình từ file .env
SECRET_KEY = os.getenv("SECRET_KEY", "321cba")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "1440")) # Mặc định 24 giờ

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Hàm tạo JWT Access Token.
    
    Args:
        data (dict): Dữ liệu cần mã hóa vào payload (ví dụ: sub, username).
        expires_delta (timedelta, optional): Thời gian sống của token. Nếu không truyền sẽ lấy mặc định.
    """
    to_encode = data.copy()
    
    # Thiết lập thời gian hết hạn (sử dụng timezone-aware datetime)
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
    to_encode.update({"exp": expire})
    
    # Mã hóa và trả về chuỗi token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)) -> dict:
    """
    Middleware xác thực JWT Token cho các API yêu cầu đăng nhập.
    """
    token = credentials.credentials
    try:
        # Giải mã và kiểm tra tính hợp lệ của Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
        
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Phiên đăng nhập đã hết hạn, vui lòng đăng nhập lại!",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token không hợp lệ!",
        )