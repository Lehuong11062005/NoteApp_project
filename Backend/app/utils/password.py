import bcrypt

def hash_password(password: str) -> str:
    # 1. Chuyển mật khẩu thành bytes và cắt chính xác 72 bytes
    pwd_bytes = password.encode('utf-8')[:72]
    # 2. Tạo salt và hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    pwd_bytes = plain_password.encode('utf-8')[:72]
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)