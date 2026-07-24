from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Xác thực mật khẩu người dùng với chuỗi đã băm (có chống lỗi UnknownHashError)"""
    if not hashed_password or not isinstance(hashed_password, str):
        return False
    safe_pass = str(plain_password)[:70]
    try:
        return pwd_context.verify(safe_pass, hashed_password)
    except Exception:
        return False

def get_password_hash(password: str) -> str:
    """Băm mật khẩu an toàn, tự động cắt ngắn nếu vượt quá giới hạn"""
    pwd_str = str(password)
    if len(pwd_str.encode('utf-8')) > 72:
        pwd_str = pwd_str[:72]
    return pwd_context.hash(pwd_str)