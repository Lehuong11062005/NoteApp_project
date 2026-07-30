import sys
import os
import tkinter as tk
from tkinter import ttk

# Thêm thư mục gốc vào PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from Frontend.controllers.auth_controller import AuthController

class LoginView(tk.Tk):
    """Giao diện màn hình Đăng nhập (Form Login)"""
    def __init__(self, controller=None):
        super().__init__()
        self.title("Đăng nhập - NoteApp")
        self.geometry("360x240")
        self.resizable(False, False)
        
        self.controller = controller if controller else AuthController(self)
        self.controller.view = self
        
        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self, text="ĐĂNG NHẬP NOTEAPP", font=("Arial", 14, "bold"), fg="#0288D1").pack(pady=15)

        frame = tk.Frame(self)
        frame.pack(padx=20, fill="x")

        tk.Label(frame, text="Tài khoản:", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=8)
        self.entry_username = ttk.Entry(frame, width=25)
        self.entry_username.grid(row=0, column=1, pady=8, padx=5)

        tk.Label(frame, text="Mật khẩu:", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=8)
        self.entry_password = ttk.Entry(frame, width=25, show="*")
        self.entry_password.grid(row=1, column=1, pady=8, padx=5)

        btn_login = tk.Button(
            self,
            text="Đăng nhập",
            bg="#0288D1",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            command=self.controller.handle_login
        )
        btn_login.pack(pady=15)
        self.bind('<Return>', lambda e: self.controller.handle_login())

if __name__ == "__main__":
    app = LoginView()
    app.mainloop()
