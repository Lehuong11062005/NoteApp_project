import tkinter as tk
from tkinter import messagebox
from Frontend.controllers.auth_controller import AuthController

class RegisterWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Đăng ký tài khoản")
        self.geometry("400x450")
        self.grab_set()
        self.auth_controller = AuthController()

        tk.Label(self, text="ĐĂNG KÝ", font=("Arial", 16, "bold")).pack(pady=20)

        tk.Label(self, text="Họ tên:").pack(anchor="w", padx=40)
        self.entry_fullname = tk.Entry(self, width=35)
        self.entry_fullname.pack(pady=5, padx=40)

        tk.Label(self, text="Email:").pack(anchor="w", padx=40)
        self.entry_email = tk.Entry(self, width=35)
        self.entry_email.pack(pady=5, padx=40)

        tk.Label(self, text="Tài khoản:").pack(anchor="w", padx=40)
        self.entry_user = tk.Entry(self, width=35)
        self.entry_user.pack(pady=5, padx=40)

        tk.Label(self, text="Mật khẩu:").pack(anchor="w", padx=40)
        self.entry_pass = tk.Entry(self, width=35, show="*")
        self.entry_pass.pack(pady=5, padx=40)

        tk.Button(self, text="Đăng ký", bg="#4CAF50", fg="white", width=20, command=self.handle_register).pack(pady=20)

    def handle_register(self):
        success, msg = self.auth_controller.register(
            self.entry_user.get().strip(), self.entry_pass.get().strip(),
            self.entry_fullname.get().strip(), self.entry_email.get().strip()
        )
        if success:
            messagebox.showinfo("Thành công", msg)
            self.destroy()
        else:
            messagebox.showerror("Lỗi", msg)