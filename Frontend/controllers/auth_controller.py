import threading
from Frontend.services.api_client import login_api, get_profile_api, logout
from Frontend.utils.messagebox import show_error

class AuthController:
    def __init__(self, view):
        self.view = view  # view hiện tại (LoginView hoặc MainView)

    # ──────────────────────────────────────────────────────────────────────
    # ĐĂNG NHẬP
    # ──────────────────────────────────────────────────────────────────────
    def handle_login(self):
        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get().strip()

        if not username or not password:
            show_error("Lỗi", "Vui lòng nhập đầy đủ thông tin!")
            return

        # Chạy API trong thread riêng để không block giao diện Tkinter
        threading.Thread(
            target=self._login_worker,
            args=(username, password),
            daemon=True
        ).start()

    def _login_worker(self, username: str, password: str):
        """Chạy trong background thread — gọi API login + profile."""
        is_success, message, status_code = login_api(username, password)

        if is_success:
            ok, profile_data = get_profile_api()
            if not ok:
                profile_data = {"username": username}
            # Trả kết quả về main thread qua after()
            self.view.after(0, lambda: self._on_login_success(profile_data))
        else:
            err_msg = message
            self.view.after(0, lambda: show_error(
                "Lỗi 401" if status_code == 401 else "Lỗi", err_msg
            ))

    def _on_login_success(self, profile_data: dict):
        """Chạy trên main thread — đóng Login, mở MainApp."""
        self.view.destroy()
        self._open_main_app(profile_data)

    def _open_main_app(self, profile_data: dict):
        """Khởi tạo MainView và cập nhật self.view sang cửa sổ mới."""
        from Frontend.views.main_view import MainView
        main_window = MainView(controller=self, profile_data=profile_data)
        self.view = main_window   # ← Cập nhật self.view sang MainView
        main_window.mainloop()

    # ──────────────────────────────────────────────────────────────────────
    # ĐĂNG XUẤT
    # ──────────────────────────────────────────────────────────────────────
    def handle_logout(self):
        """Xóa token và quay lại màn hình đăng nhập."""
        logout()                  # Xóa CURRENT_JWT_TOKEN
        main_window = self.view   # self.view lúc này là MainView
        main_window.destroy()     # Đóng MainView

        # Mở lại LoginView
        from Frontend.views.login_view import LoginView
        login_window = LoginView()
        self.view = login_window  # ← Cập nhật self.view sang LoginView mới
        login_window.mainloop()