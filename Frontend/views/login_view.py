import tkinter as tk
from tkinter import messagebox
from controllers.auth_controller import AuthController
from views.register_view import RegisterWindow

class LoginWindow(tk.Tk):
    def __init__(self, on_success_callback):
        super().__init__()
        self.title("Đăng nhập")
        self.geometry("380x350")
        self.on_success_callback = on_success_callback
        self.auth_controller = AuthController()

        tk.Label(self, text="ĐĂNG NHẬP", font=("Arial", 16, "bold"), fg="#2196F3").pack(pady=25)

        tk.Label(self, text="Tài khoản:").pack(anchor="w", padx=40)
        self.entry_user = tk.Entry(self, width=32, font=("Arial", 11))
        self.entry_user.pack(pady=5, padx=40)

        tk.Label(self, text="Mật khẩu:").pack(anchor="w", padx=40)
        self.entry_pass = tk.Entry(self, width=32, font=("Arial", 11), show="*")
        self.entry_pass.pack(pady=5, padx=40)

        tk.Button(self, text="Đăng nhập", bg="#2196F3", fg="white", font=("Arial", 11, "bold"), width=18, command=self.handle_login).pack(pady=20)
        tk.Button(self, text="Chưa có tài khoản? Đăng ký", fg="blue", relief="flat", command=lambda: RegisterWindow(self)).pack()

    def handle_login(self):
        success, result = self.auth_controller.login(self.entry_user.get().strip(), self.entry_pass.get().strip())
        if success:
            messagebox.showinfo("Thành công", f"Xin chào, {result.fullname}!")
            self.destroy()
            self.on_success_callback(result) # Truyền user sang Main App
        else:
            messagebox.showerror("Lỗi", result)