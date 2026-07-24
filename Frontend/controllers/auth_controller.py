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
            self.view.destroy() 
        else:
            display_msg = message
            
            if isinstance(message, list):
                error_msgs = [err.get("msg", "Lỗi dữ liệu") for err in message if isinstance(err, dict)]
                display_msg = "\n".join(error_msgs) if error_msgs else "Dữ liệu không hợp lệ."
            elif isinstance(message, dict):
                display_msg = message.get("detail", "Đăng nhập thất bại.")

            if status_code == 401 or status_code == 422:
                show_error("Thông báo", display_msg)
            else:
                show_error("Lỗi đăng nhập", display_msg)