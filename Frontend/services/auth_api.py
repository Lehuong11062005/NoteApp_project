from Frontend.services.api_client import APIClient

class AuthAPI:
    @staticmethod
    def login(username, password):
        # Dùng APIClient.post thay vì requests.post
        # Không cần viết Base URL hay timeout nữa vì APIClient đã lo
        res = APIClient.post("/api/auth/login", data={"username": username, "password": password})
        
        if res.status_code == 200:
            data = res.json()
            # Quan trọng: Lưu token lại để dùng cho các request sau
            if "access_token" in data:
                APIClient.set_token(data["access_token"])
            return True, data
            
        # Xử lý an toàn khi Server trả về lỗi không phải chuẩn JSON
        try:
            error_msg = res.json().get("detail", "Sai tài khoản hoặc mật khẩu")
        except ValueError:
            error_msg = "Không thể kết nối đến máy chủ hoặc lỗi hệ thống."
            
        return False, error_msg

    @staticmethod
    def register(username, password, fullname, email):
        res = APIClient.post("/api/auth/register", data={
            "username": username, 
            "password": password, 
            "fullname": fullname, 
            "email": email
        })
        
        # Bắt cả mã 200 (OK) và 201 (Created)
        if res.status_code in (200, 201):
            return True, "Đăng ký thành công!"
            
        try:
            error_msg = res.json().get("detail", "Lỗi đăng ký tài khoản")
        except ValueError:
            error_msg = "Không thể kết nối đến máy chủ hoặc lỗi hệ thống."
            
        return False, error_msg

    @staticmethod
    def get_profile():
        res = APIClient.get("/api/user/profile")
        
        if res.status_code == 200:
            return True, res.json()
            
        try:
            error_msg = res.json().get("detail", "Không thể lấy thông tin người dùng")
        except ValueError:
            error_msg = "Lỗi kết nối hoặc phiên đăng nhập đã hết hạn."
            
        return False, error_msg