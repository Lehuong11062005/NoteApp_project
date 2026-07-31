import os
import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from dotenv import load_dotenv

load_dotenv()

# Lấy chìa khóa SECRET_KEY và ALGORITHM từ file .env
SECRET_KEY = os.getenv("SECRET_KEY", "321cba")  # Giá trị mặc định nếu không có trong .env
ALGORITHM = os.getenv("ALGORITHM", "HS256")

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """
    Middleware xác thực JWT Token cho các API yêu cầu đăng nhập.
    """
    token = credentials.credentials
    try:
        # Giải mã và kiểm tra tính hợp lệ của Token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Trả về thông tin người dùng trong Token
        
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