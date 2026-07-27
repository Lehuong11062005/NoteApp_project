import tkinter as tk
from tkinter import ttk

class RegisterView(tk.Toplevel):
    def __init__(self, parent, controller=None):
        super().__init__(parent)
        self.controller = controller
        
        self.title("Đăng ký tài khoản")
        self.geometry("380x350")  # Tăng chiều cao để vừa ô Email
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self._build_ui()

    def _build_ui(self):
        title_label = tk.Label(
            self, 
            text="ĐĂNG KÝ TÀI KHOẢN", 
            font=("Arial", 14, "bold"),
            fg="#2C3E50"
        )
        title_label.pack(pady=(20, 15))

        form_frame = tk.Frame(self)
        form_frame.pack(padx=35, fill="x")

        # Ô nhập Tên đăng nhập
        tk.Label(form_frame, text="Tên đăng nhập:", font=("Arial", 10)).pack(anchor="w")
        self.entry_username = ttk.Entry(form_frame, font=("Arial", 10))
        self.entry_username.pack(fill="x", pady=(2, 8))

        # Ô nhập Email (MỚI THÊM)
        tk.Label(form_frame, text="Email:", font=("Arial", 10)).pack(anchor="w")
        self.entry_email = ttk.Entry(form_frame, font=("Arial", 10))
        self.entry_email.pack(fill="x", pady=(2, 8))

        # Ô nhập Mật khẩu
        tk.Label(form_frame, text="Mật khẩu (≥ 8 ký tự):", font=("Arial", 10)).pack(anchor="w")
        self.entry_password = ttk.Entry(form_frame, show="*", font=("Arial", 10))
        self.entry_password.pack(fill="x", pady=(2, 15))

        # Nút bấm Đăng ký
        self.btn_register = ttk.Button(
            form_frame, 
            text="Đăng ký", 
            command=self._on_register_click
        )
        self.btn_register.pack(fill="x", ipady=3)

    def _on_register_click(self):
        if self.controller:
            self.controller.handle_register()