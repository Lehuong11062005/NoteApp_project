from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from app.repositories.user_repository import UserRepository
import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Khai báo scheme — FastAPI tự thêm nút "Authorize" trên Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    Middleware dependency: Giải mã JWT token, lấy user từ DB.
    Dùng Depends(get_current_user) ở các route cần xác thực.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token không hợp lệ hoặc đã hết hạn!",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        # Giải mã token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    # Lấy user từ DB thông qua UserRepository
    user_repo = UserRepository()
    user = user_repo.find_by_username(username)
    if user is None:
        raise credentials_exception

    return user
