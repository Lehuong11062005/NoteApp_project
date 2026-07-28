import os
from dotenv import load_dotenv

import requests

class APIClient:
    # Lấy biến của mỗi trường  link của backend
    load_dotenv()
    Base_URL=os.getenv("BASE_URL")

    _token = None

    @staticmethod
    def check_server():
        try:
            response=requests.get(f"{APIClient.Base_URL}")
            if response.status_code== 200:
                return True,'Kết nối thành công'
            return False,f"Loi ket noi  database {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False,"Khong the ket noi  database"
     @classmethod
    def set_token(cls, token):
        cls._token = token

    @classmethod
    def get_headers(cls):
        headers = {"Content-Type": "application/json"}
        if cls._token:
            headers["Authorization"] = f"Bearer {cls._token}"
        return headers

    @classmethod
    def get(cls, endpoint):
        return requests.get(f"{cls.Base_URL}{endpoint}", headers=cls.get_headers())

    @classmethod
    def post(cls, endpoint, data):
        return requests.post(f"{cls.Base_URL}{endpoint}", json=data, headers=cls.get_headers())
