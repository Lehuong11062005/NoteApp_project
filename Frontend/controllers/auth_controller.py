import re
from Frontend.services.auth_api import AuthAPI
from Frontend.utils.messagebox import show_success, show_error

class AuthController:
    def __init__(self, view=None):
        self.view = view

    def _is_valid_email(self, email: str) -> bool:
        """Hàm kiểm tra định dạng email bằng Regex"""
        pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        return re.match(pattern, email) is not None

    # ==================== 1. XỬ LÝ ĐĂNG KÝ ====================
    def handle_register(self):
        username = self.view.entry_username.get().strip()
        email = self.view.entry_email.get().strip()
        password = self.view.entry_password.get().strip()

        # Validation
        if not username or not email or not password:
            show_error("Lỗi", "Vui lòng nhập đầy đủ Tên đăng nhập, Email và Mật khẩu!")
            return

        if not self._is_valid_email(email):
            show_error("Lỗi", "Định dạng Email không hợp lệ!")
            return

        if len(password) < 6:
            show_error("Lỗi", "Mật khẩu phải chứa ít nhất 6 ký tự!")
            return

        # Gọi API Đăng ký
        is_success, message = AuthAPI.register(username, email, password)
        if is_success:
            show_success("Thành công", message)
            self.view.destroy()
        else:
            show_error("Lỗi đăng ký", message)

    # ==================== 2. XỬ LÝ ĐĂNG NHẬP (THÊM MỚI) ====================
    def handle_login(self):
        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get().strip()

        # Validation
        if not username or not password:
            show_error("Lỗi", "Vui lòng nhập Tên đăng nhập và Mật khẩu!")
            return

        # Gọi API Đăng nhập
        is_success, message = AuthAPI.login(username, password)
        if is_success:
            show_success("Thành công", message)
            self.view.destroy()
        else:
            show_error("Lỗi đăng nhập", message)