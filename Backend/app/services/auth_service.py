from app.repositories.user_repository import UserRepository
from app.utils.password import hash_password

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, username: str, email: str, password: str):
        # 1. Kiểm tra username hoặc email đã tồn tại chưa
        if self.user_repo.find_by_username(username):
            return False, "Tên đăng nhập đã tồn tại!"
        
        if self.user_repo.find_by_email(email):
            return False, "Email đã được sử dụng!"

        # 2. Hash mật khẩu và lưu người dùng
        hashed_pwd = hash_password(password)
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_pwd
        }
        self.user_repo.create_user(user_data)
        return True, "Đăng ký tài khoản thành công!"