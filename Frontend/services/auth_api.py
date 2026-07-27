import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
TIMEOUT_SECONDS = 5

class AuthAPI:
    @staticmethod
    def check_server():
        """Kiểm tra xem Backend server có đang kết nối được không"""
        try:
            response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT_SECONDS)
            if response.status_code == 200:
                return True, response.json()
            return False, "Server phản hồi lỗi"
        except Exception as e:
            return False, str(e)

    @staticmethod
    def _send_auth_request(endpoint: str, payload: dict):
        url = f"{BASE_URL}/auth/{endpoint}"
        try:
            response = requests.post(url, json=payload, timeout=TIMEOUT_SECONDS)
            
            # Thử parse JSON từ response
            try:
                data = response.json()
            except Exception:
                return False, f"Server trả về lỗi ({response.status_code})"

            if response.status_code in [200, 201]:
                return True, data.get("message", "Thành công!")
            
            error_detail = data.get("detail", "Thao tác thất bại!")
            return False, error_detail

        except requests.exceptions.Timeout:
            return False, "Lỗi: Yêu cầu API đã hết thời gian chờ"
        except requests.exceptions.RequestException as e:
            return False, f"Lỗi kết nối API: {str(e)}"
        except Exception as e:
            return False, f"Lỗi không xác định: {str(e)}"

    @staticmethod
    def register(username: str, email: str, password: str):
        payload = {
            "username": username,
            "email": email,
            "password": password
        }
        return AuthAPI._send_auth_request("register", payload)

    @staticmethod
    def login(username: str, password: str):
        payload = {
            "username": username,
            "password": password
        }
        return AuthAPI._send_auth_request("login", payload)