import requests
from Frontend.services.api_client import APIClient

def login_api(username, password):
    # Sử dụng đúng biến Base_URL từ class APIClient gốc
    base_url = str(APIClient.Base_URL).rstrip('/') if APIClient.Base_URL else "http://127.0.0.1:8000"
    url = f"{base_url}/api/auth/login"
    payload = {"username": username, "password": password}
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data.get("message", "Đăng nhập thành công!"), 200
        else:
            try:
                error_detail = response.json().get("detail", "Đăng nhập thất bại!")
            except Exception:
                error_detail = "Tài khoản hoặc mật khẩu không chính xác!"
            return False, error_detail, response.status_code
    except requests.exceptions.ConnectionError:
        return False, "Không thể kết nối đến máy chủ Backend!", 500
    except Exception as e:
        return False, f"Lỗi: {str(e)}", 500