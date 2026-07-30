import requests
from Frontend.services.api_client import APIClient

class AuthAPI:
    @staticmethod
    def login(username, password):
        url = f"{APIClient.BASE_URL}/api/auth/login"
        try:
            res = requests.post(url, json={"username": username, "password": password}, timeout=APIClient.TIMEOUT)
            if res.status_code == 200:
                return True, res.json()
            return False, res.json().get("detail", "Sai tài khoản hoặc mật khẩu")
        except Exception as e:
            return False, str(e)

    @staticmethod
    def register(username, password, fullname, email):
        url = f"{APIClient.BASE_URL}/api/auth/register"
        try:
            res = requests.post(url, json={
                "username": username, "password": password, 
                "fullname": fullname, "email": email
            }, timeout=APIClient.TIMEOUT)
            if res.status_code == 200:
                return True, "Đăng ký thành công!"
            return False, res.json().get("detail", "Lỗi đăng ký")
        except Exception as e:
            return False, str(e)