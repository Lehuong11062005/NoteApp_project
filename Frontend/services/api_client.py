import os
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv

# Load môi trường ở cấp độ module (trước khi class được định nghĩa)
load_dotenv()

class APIClient:
    # Lấy BASE_URL, có thêm fallback mặc định trong trường hợp mất file .env
    BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
    TIMEOUT = 5

    _token = None  # Lưu trữ JWT Token sau khi Đăng nhập

    @classmethod
    def check_server(cls) -> tuple[bool, str]:
        """Kiểm tra kết nối đến Backend Server."""
        try:
            # Chỉ cần gọi đến gốc URL để test server còn sống không
            response = requests.get(cls.BASE_URL, timeout=cls.TIMEOUT)
            if response.status_code == 200:
                return True, 'Kết nối server thành công'
            return False, f"Lỗi phản hồi từ server: {response.status_code}"
        except requests.exceptions.Timeout:
            return False, "Hết thời gian chờ kết nối. Server phản hồi quá chậm."
        except requests.exceptions.ConnectionError:
            return False, "Không thể kết nối đến Server (Server có thể chưa bật)."
        except Exception as e:
            return False, f"Lỗi hệ thống: {str(e)}"

    @classmethod
    def set_token(cls, token: str):
        """Lưu Token khi Đăng nhập thành công"""
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
    def get_headers(cls) -> dict:
        """Tự động tạo Header chứa Bearer Token"""
        headers = {"Content-Type": "application/json"}
        if cls._token:
            headers["Authorization"] = f"Bearer {cls._token}"
        return headers

    @classmethod
    def _safe_request(cls, method: str, endpoint: str, **kwargs):
        """
        Hàm dùng chung cho mọi Request để chống trùng lặp code
        và bắt lỗi mất mạng, tránh làm crash ứng dụng Frontend.
        """
        url = f"{cls.BASE_URL}{endpoint}"
        kwargs.setdefault("headers", cls.get_headers())
        kwargs.setdefault("timeout", cls.TIMEOUT)

        try:
            return requests.request(method, url, **kwargs)
        except RequestException:
            # Tạo một object mock response để Controller bên ngoài có thể 
            # đọc được status_code = 503 mà không bị văng lỗi code
            error_response = requests.Response()
            error_response.status_code = 503
            error_response._content = b'{"detail": "Khong the ket noi den may chu Backend"}'
            return error_response

    @classmethod
    def get(cls, endpoint: str, params=None):
        return cls._safe_request("GET", endpoint, params=params)

    @classmethod
    def post(cls, endpoint: str, data=None):
        return cls._safe_request("POST", endpoint, json=data)

    @classmethod
    def put(cls, endpoint: str, data=None):
        return cls._safe_request("PUT", endpoint, json=data)

    @classmethod
    def delete(cls, endpoint: str):
        return cls._safe_request("DELETE", endpoint)