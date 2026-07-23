import os
import requests
from dotenv import load_dotenv

class APIClient:
    # Lấy biến môi trường link của backend
    load_dotenv()
    Base_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
    
    # Biến lưu trữ JWT Token sau khi đăng nhập thành công
    token = None

    @classmethod
    def set_token(cls, token: str):
        """Lưu token sau khi đăng nhập thành công"""
        cls.token = token

    @classmethod
    def clear_token(cls):
        """Xóa token khi đăng xuất"""
        cls.token = None

    @classmethod
    def _get_headers(cls, custom_headers=None):
        """Tự động đính kèm Authorization Header nếu có token"""
        headers = custom_headers.copy() if custom_headers else {}
        if cls.token:
            headers["Authorization"] = f"Bearer {cls.token}"
        return headers

    @staticmethod
    def check_server():
        try:
            response = requests.get(f"{APIClient.Base_URL}")
            if response.status_code == 200:
                return True, 'Kết nối thành công'
            return False, f"Loi ket noi database {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Khong the ket noi database"

    # Các hàm gửi Request tự động đính kèm Token 
    @classmethod
    def get(cls, endpoint, params=None, headers=None):
        url = f"{cls.Base_URL}{endpoint}"
        return requests.get(url, params=params, headers=cls._get_headers(headers))

    @classmethod
    def post(cls, endpoint, json=None, data=None, headers=None):
        url = f"{cls.Base_URL}{endpoint}"
        return requests.post(url, json=json, data=data, headers=cls._get_headers(headers))

    @classmethod
    def put(cls, endpoint, json=None, headers=None):
        url = f"{cls.Base_URL}{endpoint}"
        return requests.put(url, json=json, headers=cls._get_headers(headers))

    @classmethod
    def delete(cls, endpoint, headers=None):
        url = f"{cls.Base_URL}{endpoint}"
        return requests.delete(url, headers=cls._get_headers(headers))

