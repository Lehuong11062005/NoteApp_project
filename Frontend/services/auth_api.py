import requests

BASE_URL = "http://127.0.0.1:8000"

def login_api(username, password):
    url = f"{BASE_URL}/auth/login"
    payload = {"username": username, "password": password}
    
    try:
        response = requests.post(url, json=payload, timeout=5)
        if response.status_code == 200:
            data = response.json()
            return True, data.get("message", "Đăng nhập thành công!")
        elif response.status_code == 401:
            return False, "Sai tài khoản hoặc mật khẩu!"
        else:
            try:
                error_detail = response.json().get("detail", "Lỗi hệ thống")
            except:
                error_detail = f"Lỗi hệ thống ({response.status_code})"
            return False, error_detail
    except requests.exceptions.ConnectionError:
        return False, "Không thể kết nối đến máy chủ Backend!"
    except requests.exceptions.Timeout:
        return False, "Kết nối tới máy chủ quá thời gian!"