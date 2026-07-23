import tkinter as tk
from tkinter import ttk

# Bỏ chữ 'Frontend.' để đồng bộ với cách gọi từ main.py
from controllers.auth_controller import AuthController

class LoginView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Đăng nhập - NoteApp")
        self.geometry("350x220")
        self.resizable(False, False)
        
        self.controller = AuthController(self)
        self._setup_ui()

    def _setup_ui(self):
        tk.Label(self, text="ĐĂNG NHẬP", font=("Arial", 14, "bold")).pack(pady=15)

        frame = tk.Frame(self)
        frame.pack(padx=20, fill="x")

        tk.Label(frame, text="Tài khoản:").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_username = ttk.Entry(frame, width=25)
        self.entry_username.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(frame, text="Mật khẩu:").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_password = ttk.Entry(frame, width=25, show="*")
        self.entry_password.grid(row=1, column=1, pady=5, padx=5)

        ttk.Button(self, text="Đăng nhập", command=self.controller.handle_login).pack(pady=20)
        
        # Cho phép người dùng nhấn phím Enter để đăng nhập nhanh
        self.bind('<Return>', lambda e: self.controller.handle_login())

if __name__ == "__main__":
    app = LoginView()
    app.mainloop()