from services.auth_api import AuthAPI
from models.user import User
from services.api_client import APIClient
class AuthController:
    def login(self, username, password):
        if not username or not password:
            return False, "Vui lòng nhập đầy đủ thông tin!"
        
        success, data = AuthAPI.login(username, password)
        if success:
            # 1. Lấy token từ response trả về của backend
            token = data.get("access_token")
            
            # 2. Lưu token vào APIClient để tự động đính kèm vào các request sau (Notes,...)
            if token:
                APIClient.set_token(token)
            
            # 3. Khởi tạo User và trả về
            user = User(username=data['user']['username'], fullname=data['user']['fullname'])
            return True, user
            
        return False, data

    def register(self, username, password, fullname, email):
        if not fullname or not email or not username or not password:
            return False, "Vui lòng điền tất cả các trường!"
        return AuthAPI.register(username, password, fullname, email)

    def logout(self):
        APIClient.clear_token()

    def get_profile(self):
        success, data = AuthAPI.get_profile()
        if success:
            user = User(
                username=data.get("username", ""),
                fullname=data.get("fullname", ""),
                email=data.get("email", "")
            )
            return True, user
        return False, data