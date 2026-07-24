from passlib.context import CryptContext

# Đổi scheme sang pbkdf2_sha256 để loại bỏ hoàn toàn giới hạn 72 bytes của bcrypt
pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")

def get_password_hash(password: str) -> str:
    """Băm mật khẩu an toàn không giới hạn độ dài"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Xác thực mật khẩu"""
    return pwd_context.verify(plain_password, hashed_password)