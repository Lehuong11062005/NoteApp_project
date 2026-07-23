from tkinter import messagebox
from services.api_client import login_api

class AuthController:
    def __init__(self, view):
        self.view = view

    def handle_login(self):
        # 1. Lấy dữ liệu từ giao diện
        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get().strip()

        # 2. Kiểm tra dữ liệu rỗng
        if not username or not password:
            messagebox.showwarning("Cảnh báo", "Vui lòng nhập đầy đủ tài khoản và mật khẩu!", parent=self.view)
            return

        # 3. Gọi API Đăng nhập
        success, message, status_code = login_api(username, password)

        # 4. Xử lý kết quả trả về
        if success:
            messagebox.showinfo("Thành công", message, parent=self.view)
            # Tạm thời đóng cửa sổ login sau khi đăng nhập thành công. 
            # (Sau này chúng ta sẽ viết code mở Dashboard ở đây)
            self.view.destroy() 
        else:
            messagebox.showerror("Lỗi đăng nhập", message, parent=self.view)