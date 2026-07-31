import os
from dotenv import load_dotenv

import requests

class APIClient:
    # Lấy biến của mỗi trường  link của backend
    load_dotenv()
    BASE_URL=os.getenv("BASE_URL")
    TIMEOUT = 5

    @staticmethod
    def check_server():
        try:
            response=requests.get(f"{APIClient.BASE_URL}")
            if response.status_code== 200:
                return True,'Kết nối thành công'
            return False,f"Loi ket noi  database {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False,"Khong the ket noi  database"

    _token = None  # Lưu trữ JWT Token sau khi Đăng nhập

    @classmethod
    def set_token(cls, token: str):
        """Lưu Token khi Đăng nhập thành công """
        cls._token = token

    @classmethod
    def get_token(cls):
        """Lấy Token hiện tại"""
        return cls._token

    @classmethod
    def clear_token(cls):
        """Xóa Token khi Đăng xuất"""
        cls._token = None

    @classmethod
    def get_headers(cls):
        """Tự động tạo Header chứa Bearer Token"""
        print(f"DEBUG - Token hiện tại trong APIClient: {cls._token}") 
        headers = {"Content-Type": "application/json"}
        if cls._token:
            headers["Authorization"] = f"Bearer {cls._token}"
        return headers
    @classmethod
    def get(cls, endpoint: str, params=None):
        url = f"{cls.BASE_URL}{endpoint}"
        return requests.get(url, headers=cls.get_headers(), params=params, timeout=cls.TIMEOUT)

    @classmethod
    def post(cls, endpoint: str, data=None):
        url = f"{cls.BASE_URL}{endpoint}"
        return requests.post(url, json=data, headers=cls.get_headers(), timeout=cls.TIMEOUT)

    @classmethod
    def put(cls, endpoint: str, data=None):
        url = f"{cls.BASE_URL}{endpoint}"
        return requests.put(url, json=data, headers=cls.get_headers(), timeout=cls.TIMEOUT)

    @classmethod
    def delete(cls, endpoint: str):
        url = f"{cls.BASE_URL}{endpoint}"
        return requests.delete(url, headers=cls.get_headers(), timeout=cls.TIMEOUT)