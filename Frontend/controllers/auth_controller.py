from Frontend.services.auth_api import login_api, register_api
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
            show_error("Thất bại", message)

    def handle_register(self):
        username = self.view.entry_username.get().strip()
        email = self.view.entry_email.get().strip() if hasattr(self.view, 'entry_email') else ""
        password = self.view.entry_password.get().strip()

        if not username or not password or not email:
            show_error("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        is_success, message, status_code = register_api(username, email, password)

        if is_success:
            show_success("Thành công", message)
            self.view.destroy()
        else:
            display_msg = message
            if isinstance(message, list):
                error_msgs = [err.get("msg", "Lỗi dữ liệu") for err in message if isinstance(err, dict)]
                display_msg = "\n".join(error_msgs) if error_msgs else "Dữ liệu không hợp lệ."
            elif isinstance(message, dict):
                display_msg = message.get("detail", "Lỗi không xác định")

            show_error("Thất bại", display_msg)