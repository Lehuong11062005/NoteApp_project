from app.repositories.user_repository import UserRepository
from app.utils.password import hash_password, verify_password

class AuthService:
    def __init__(self):
        self.user_repo = UserRepository()

    def register_user(self, username: str, password: str):
        if self.user_repo.find_by_username(username):
            return False, "Tên đăng nhập đã tồn tại!"

        hashed_pwd = hash_password(password)
        user_data = {
            "username": username,
            "password": hashed_pwd
        }
        self.user_repo.create_user(user_data)
        return True, "Đăng ký tài khoản thành công!"

    def login_user(self, username: str, password: str):
        user = self.user_repo.find_by_username(username)
        if not user or not verify_password(password, user["password"]):
            return False, "Tên đăng nhập hoặc mật khẩu không đúng!"

        return True, "Đăng nhập thành công!"