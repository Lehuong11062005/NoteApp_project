from tkinter import messagebox
from Frontend.views.register_view import RegisterView
from Frontend.services.api_client import APIClient

class AuthController:
    def __init__(self, root):
        self.root = root
        # Đưa giao diện vào cửa sổ chính
        self.view = RegisterView(self.root, self)
        
    def handle_register(self):
        data = self.view.get_input_data()
        
        # Kiểm tra Client-side cơ bản xem điền đủ chưa
        if not data["username"] or not data["email"] or not data["password"]:
            messagebox.showwarning("Thông báo", "Vui lòng nhập đầy đủ thông tin!")
            return
            
        # Gọi sang lớp dịch vụ mạng (API Client)
        response = APIClient.register_user(data["username"], data["email"], data["password"])
        
        if response is None:
            messagebox.showerror("Lỗi kết nối", "Không thể kết nối đến Server Backend!")
            return
            
        if response.status_code == 201:
            messagebox.showinfo("Thành công", response.json().get("message"))
            self.view.clear_fields()  # Đăng ký xong thì xóa trắng form
        else:
            # Hiện lỗi trả về từ FastAPI (Ví dụ: Trùng username)
            error_detail = response.json().get("detail", "Đăng ký không thành công.")
            messagebox.showerror("Thất bại", error_detail)