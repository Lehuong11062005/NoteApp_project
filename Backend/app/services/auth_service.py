from app.repositories.user_repository import UserRepository
from app.utils.password import hash_password
from app.utils.password import verify_password, hash_password
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
    def login_user(self, username, password):
        # 1. Tìm user trong cơ sở dữ liệu
        user = self.user_repo.find_by_username(username) # Hoặc phương thức tìm user tương đương trong repo của bạn
        if not user:
            return False, "Tài khoản hoặc mật khẩu không chính xác!"

        # 2. Kiểm tra mật khẩu (dùng hàm verify_password trong utils/password.py)
        if not verify_password(password, user["password"]):
            return False, "Tài khoản hoặc mật khẩu không chính xác!"

        return True, "Đăng nhập thành công!"