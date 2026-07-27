import os
import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
CURRENT_JWT_TOKEN = None

class APIClient:
    Base_URL = BASE_URL

    @staticmethod
    def check_server():
        try:
            response = requests.get(f"{APIClient.Base_URL}/", timeout=5)
            if response.status_code == 200:
                return True, 'Kết nối thành công'
            return False, f"Lỗi kết nối database {response.status_code}"
        except requests.exceptions.ConnectionError:
            return False, "Không thể kết nối database"

def login_api(username, password):
    global CURRENT_JWT_TOKEN
    url = f"{BASE_URL}/api/auth/login"
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
    except Exception as e:
        return False, f"Lỗi: {str(e)}", 500

def get_profile_api():
    """Gọi GET /api/auth/profile với Bearer token hiện tại."""
    global CURRENT_JWT_TOKEN
    if not CURRENT_JWT_TOKEN:
        return False, "Chưa đăng nhập!"
    
    url = f"{BASE_URL}/api/auth/profile"
    headers = {"Authorization": f"Bearer {CURRENT_JWT_TOKEN}"}
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        if response.status_code == 200:
            return True, response.json()
        elif response.status_code == 401:
            return False, "Token hết hạn hoặc không hợp lệ!"
        else:
            return False, f"Lỗi hệ thống ({response.status_code})"
    except requests.exceptions.ConnectionError:
        return False, "Không thể kết nối đến máy chủ Backend!"
    except Exception as e:
        return False, f"Lỗi: {str(e)}"

def logout():
    """Xóa token khỏi bộ nhớ (đăng xuất phía Client)."""
    global CURRENT_JWT_TOKEN
    CURRENT_JWT_TOKEN = None

def upload_image_api(file_path: str):
    """Gửi file ảnh từ file_path lên API POST /api/upload.
    Trả về (is_success: bool, url_or_msg: str)
    """
    url = f"{BASE_URL}/api/upload"
    global CURRENT_JWT_TOKEN
    headers = {}
    if CURRENT_JWT_TOKEN:
        headers["Authorization"] = f"Bearer {CURRENT_JWT_TOKEN}"

    try:
        if not os.path.exists(file_path):
            return False, "File ảnh không tồn tại!"

        with open(file_path, "rb") as f:
            files = {"file": (os.path.basename(file_path), f, "image/jpeg")}
            response = requests.post(url, files=files, headers=headers, timeout=15)

        if response.status_code == 200:
            data = response.json()
            image_url = data.get("url") or data.get("data", {}).get("url")
            return True, image_url
        else:
            return False, f"Upload thất bại ({response.status_code})"
    except requests.exceptions.ConnectionError:
        return False, "Không thể kết nối đến máy chủ Backend!"
    except Exception as e:
        return False, f"Lỗi upload: {str(e)}"
