import hashlib
import hmac

# Dùng cùng SECRET_KEY với JWT để nhất quán
SECRET_KEY = "SECRET_KEY_CUA_NHOM"

def get_password_hash(password: str) -> str:
    """Mã hóa password bằng HMAC-SHA256.
    Không giới hạn độ dài, không cần thư viện ngoài."""
    return hmac.new(
        SECRET_KEY.encode("utf-8"),
        password.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """So sánh password an toàn (chống timing attack)."""
    return hmac.compare_digest(
        get_password_hash(plain_password),
        hashed_password
    )