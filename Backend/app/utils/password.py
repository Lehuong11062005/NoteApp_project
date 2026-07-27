import hashlib
import hmac

SECRET_KEY = "SECRET_KEY_CUA_NHOM"

def get_password_hash(password: str) -> str:
    """Mã hóa password bằng HMAC-SHA256."""
    return hmac.new(
        SECRET_KEY.encode("utf-8"),
        password.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """So sánh password an toàn."""
    return hmac.compare_digest(
        get_password_hash(plain_password),
        hashed_password
    )
