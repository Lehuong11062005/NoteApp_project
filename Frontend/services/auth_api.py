import requests

BASE_URL = "http://127.0.0.1:8000"

def register_api(username, password, email=None, full_name=None):
    url = f"{BASE_URL}/auth/register"
    
    payload = {"username": username, "password": password}
    if email:
        payload["email"] = email
    if full_name:
        payload["full_name"] = full_name
        
    try:
        # Timeout 5s giúp tránh treo UI Tkinter
        response = requests.post(url, json=payload, timeout=5)
        
        # 1. Đăng ký thành công (chấp nhận cả HTTP 200 và 201)
        if response.status_code in (200, 201):
            return True, "Đăng ký tài khoản thành công!"
        
        # 2. Lỗi trùng lặp dữ liệu (Username / Email đã tồn tại)
        elif response.status_code == 409:
            return False, "Tên đăng nhập hoặc Email đã tồn tại!"
            
        # 3. Lỗi Validation của FastAPI (Pydantic / Schema)
        elif response.status_code == 422:
            return False, "Dữ liệu không hợp lệ (Kiểm tra lại định dạng Email hoặc Mật khẩu)!"
            
        # 4. Các lỗi HTTP khác
        else:
            try:
                res_data = response.json()
                # Lấy message tùy chỉnh của Backend trước, nếu không có mới lấy detail của FastAPI
                error_detail = res_data.get("message") or res_data.get("detail") or "Lỗi hệ thống"
            except Exception:
                error_detail = f"Lỗi máy chủ ({response.status_code})"
                
            return False, error_detail
            
    except requests.exceptions.ConnectionError:
        return False, "Không thể kết nối đến máy chủ Backend (Chưa bật Server)!"
    except requests.exceptions.Timeout:
        return False, "Kết nối tới máy chủ quá thời gian (Timeout)!"
    except Exception as e:
        return False, f"Lỗi không xác định: {str(e)}"