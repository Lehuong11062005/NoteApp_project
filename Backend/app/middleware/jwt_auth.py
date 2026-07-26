from fastapi import Security, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

# Cấu hình bảo mật cơ bản
security = HTTPBearer()
SECRET_KEY = "khoa_bi_mat_cua_nhom" # Ghi chú: Đổi thành biến môi trường trong file .env sau
ALGORITHM = "HS256"

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        # Giải mã và kiểm tra token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token đã hết hạn")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Token không hợp lệ")