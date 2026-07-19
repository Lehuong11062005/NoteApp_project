from Frontend.services.api_client import login_api
from Frontend.utils.messagebox import show_success, show_error

class AuthController:
    def __init__(self, view):
        self.view = view

    def handle_login(self):
        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get().strip()

        if not username or not password:
            show_error("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        is_success, message, status_code = login_api(username, password)

        if is_success:
            show_success("Thành công", message)
            self.view.destroy() # Đóng form login (Sau này sẽ gọi code mở form chính ở đây)
        else:
            if status_code == 401:
                show_error("Lỗi 401", message)
            else:
                show_error("Lỗi", message)