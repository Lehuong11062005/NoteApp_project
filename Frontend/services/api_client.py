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