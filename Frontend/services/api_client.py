import os
import requests
from dotenv import load_dotenv

load_dotenv()

class APIClient:
    # Lấy biến môi trường, nếu không có sẽ tự động dùng localhost:8000
    Base_URL = os.getenv("BASE_URL", "http://localhost:8000")

    @staticmethod
    def check_server():
        try:
            response = requests.get(f"{APIClient.Base_URL}")
            if response.status_code == 200:
                return True, 'Kết nối thành công'
            return False, f"Lỗi kết nối server: {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Không thể kết nối đến server Backend"

# ==========================================
# CÁC HÀM XỬ LÝ ĐĂNG NHẬP VÀ XÁC THỰC (JWT)
# ==========================================

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
CURRENT_JWT_TOKEN = None 

def login_api(username, password):
    global CURRENT_JWT_TOKEN
    url = f"{BASE_URL}/auth/login"
    payload = {"username": username, "password": password}
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            CURRENT_JWT_TOKEN = response.json().get("access_token")
            return True, "Đăng nhập thành công!", 200
        elif response.status_code == 401:
            return False, "Sai tài khoản hoặc mật khẩu!", 401
        else:
            return False, f"Lỗi hệ thống ({response.status_code})", response.status_code
    except requests.exceptions.ConnectionError:
        return False, "Không thể kết nối đến máy chủ Backend!", 0

def get_profile_api():
    """Gọi GET /auth/profile với Bearer token hiện tại.
    Trả về: (is_success: bool, data: dict | error_msg: str)"""
    global CURRENT_JWT_TOKEN
    if not CURRENT_JWT_TOKEN:
        return False, "Chưa đăng nhập!"
    
    url = f"{BASE_URL}/auth/profile"
    headers = {"Authorization": f"Bearer {CURRENT_JWT_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return True, response.json()  # dict: {user_id, username, email, ...}
        elif response.status_code == 401:
            return False, "Token hết hạn hoặc không hợp lệ!"
        else:
            return False, f"Lỗi hệ thống ({response.status_code})"
    except requests.exceptions.ConnectionError:
        return False, "Không thể kết nối đến máy chủ Backend!"

def logout():
    """Xóa token khỏi bộ nhớ (đăng xuất phía Client).
    Sau khi gọi hàm này, mọi API cần xác thực đều sẽ thất bại."""
    global CURRENT_JWT_TOKEN
    CURRENT_JWT_TOKEN = None