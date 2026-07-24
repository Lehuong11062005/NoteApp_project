from tkinter import messagebox
# Sửa dòng này: Import hàm register_api thay vì AuthAPI
from services.auth_api import register_api 

class AuthController:
    def __init__(self, view):
        self.view = view

    def handle_register(self):
        # 1. Lấy dữ liệu người dùng nhập từ View
        data = self.view.get_register_data()

        # 2. Validate nhanh phía Client
        if not data["username"] or not data["password"]:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ Tài khoản và Mật khẩu!")
            return

        # 3. Gọi hàm register_api
        is_success, message = register_api(
            username=data["username"],
            password=data["password"],
            email=data["email"],
            full_name=data["full_name"]
        )

        # 4. Hiển thị thông báo
        if is_success:
            messagebox.showinfo("Thành công", message)
            self.view.destroy()  # Đóng cửa sổ Đăng ký sau khi xong
        else:
            messagebox.showerror("Lỗi đăng ký", message)