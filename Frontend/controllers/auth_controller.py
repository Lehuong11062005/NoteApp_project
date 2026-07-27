import threading
from Frontend.services.api_client import login_api, get_profile_api, logout
from Frontend.utils.messagebox import show_error, show_success

class AuthController:
    def __init__(self, view=None):
        self.view = view  # view hiện tại (LoginView hoặc MainView)

    def handle_login(self):
        """Xử lý sự kiện đăng nhập khi người dùng nhấn nút Đăng nhập."""
        username = self.view.entry_username.get().strip()
        password = self.view.entry_password.get().strip()

        if not username or not password:
            show_error("Lỗi", "Vui lòng nhập đầy đủ thông tin tài khoản và mật khẩu!")
            return

        # Chạy trong thread riêng để tránh treo giao diện Tkinter
        threading.Thread(
            target=self._login_worker,
            args=(username, password),
            daemon=True
        ).start()

    def _login_worker(self, username: str, password: str):
        """Worker thread: gọi API login + profile."""
        is_success, message, status_code = login_api(username, password)

        if is_success:
            # Lấy thông tin profile user đăng nhập thành công
            ok, profile_data = get_profile_api()
            if not ok:
                profile_data = {"username": username}

            # Trả kết quả về main thread Tkinter bằng after()
            self.view.after(0, lambda: self._on_login_success(profile_data))
        else:
            err_msg = message if isinstance(message, str) else "Đăng nhập thất bại!"
            self.view.after(0, lambda: show_error("Lỗi đăng nhập", err_msg))

    def _on_login_success(self, profile_data: dict):
        """Tắt Form Login -> Mở Main App."""
        login_window = self.view
        login_window.destroy()  # Tắt cửa sổ Login

        self._open_main_app(profile_data)

    def _open_main_app(self, profile_data: dict):
        """Khởi tạo và mở cửa sổ Main App."""
        from Frontend.views.main_view import MainView
        main_window = MainView(controller=self, profile_data=profile_data)
        self.view = main_window
        main_window.mainloop()

    def handle_logout(self):
        """Đăng xuất: Xóa token JWT và quay lại màn hình Đăng nhập."""
        logout()  # Xóa token phía client
        
        main_window = self.view
        if main_window:
            main_window.destroy()  # Tắt cửa sổ MainApp

        # Mở lại màn hình Đăng nhập (LoginView)
        from Frontend.views.login_view import LoginView
        login_window = LoginView()
        self.view = login_window
        login_window.mainloop()