import os
from dotenv import load_dotenv
import requests

class APIClient:
    load_dotenv()
    Base_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

    @staticmethod
    def check_server():
        try:
            response = requests.get(f"{APIClient.Base_URL}")
            if response.status_code == 200:
                return True, 'Kết nối thành công'
            return False, f"Lỗi kết nối database {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Không thể kết nối database"

    @staticmethod
    def login_api(username, password):
        base = APIClient.Base_URL.rstrip('/')
        url = f"{base}/api/auth/login" if not base.endswith('/api') else f"{base}/auth/login"
        payload = {"username": username, "password": password}
        
        try:
            response = requests.post(url, json=payload, timeout=5)
            status_code = response.status_code
            
            if status_code == 200:
                data = response.json()
                return True, data.get("message", "Đăng nhập thành công!"), status_code
            else:
                try:
                    error_detail = response.json().get("detail", "Sai tài khoản hoặc mật khẩu!")
                except:
                    error_detail = "Lỗi hệ thống từ phía server."
                return False, error_detail, status_code
                
        except requests.exceptions.ConnectionError:
            return False, "Không thể kết nối đến máy chủ Backend!", 500
        except requests.exceptions.Timeout:
            return False, "Kết nối tới máy chủ quá thời gian!", 508

def login_api(username, password):
    return APIClient.login_api(username, password)