import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk

# Tự động thêm đường dẫn module Frontend vào sys.path
sys.path.append(str(Path(__file__).resolve().parent))

from services.auth_api import AuthAPI
from controllers.auth_controller import AuthController
from views.register import RegisterView


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Hệ thống Xác thực - NoteApp")
        self.geometry("380x280")
        self.resizable(False, False)

        # 1. Kiểm tra trạng thái Backend
        self._check_backend_status()

        # 2. Xây dựng giao diện Auth
        self._build_ui()

    def _check_backend_status(self):
        is_alive, data = AuthAPI.check_server()
        if is_alive:
            msg = data.get("message", "Server đang hoạt động") if isinstance(data, dict) else str(data)
            status_text = f"✅ {msg}"
            status_color = "#27AE60"
        else:
            status_text = f"❌ Lỗi kết nối Backend: {data}"
            status_color = "#C0392B"

        lbl_status = tk.Label(self, text=status_text, fg=status_color, font=("Arial", 9, "italic"))
        lbl_status.pack(pady=(15, 5))

    def _build_ui(self):
        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both", padx=40, pady=10)

        title = tk.Label(frame, text="TÀI KHOẢN", font=("Arial", 14, "bold"), fg="#2C3E50")
        title.pack(pady=(10, 20))

        # Nút Đăng ký
        btn_register = ttk.Button(frame, text="Đăng ký tài khoản mới", command=self.open_register_window)
        btn_register.pack(fill="x", ipady=6, pady=6)

        # Nút Đăng nhập
        btn_login = ttk.Button(frame, text="Đăng nhập", command=self.open_login_window)
        btn_login.pack(fill="x", ipady=6, pady=6)

    def open_register_window(self):
        reg_view = RegisterView(self)
        controller = AuthController(reg_view)
        reg_view.controller = controller

    def open_login_window(self):
        # Mở view Đăng nhập khi cần
        pass


if __name__ == "__main__":
    app = MainApp()
    app.mainloop()