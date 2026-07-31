from Frontend.services.auth_api import AuthAPI
from Frontend.models.user import User

class AuthController:
    def login(self, username, password):
        if not username or not password:
            return False, "Vui lòng nhập đầy đủ thông tin!"
        
        success, data = AuthAPI.login(username, password)
        if success:
            user = User(username=data['user']['username'], fullname=data['user']['fullname'])
            return True, user
        return False, data

    def register(self, username, password, fullname, email):
        if not fullname or not email or not username or not password:
            return False, "Vui lòng điền tất cả các trường!"
        return AuthAPI.register(username, password, fullname, email)