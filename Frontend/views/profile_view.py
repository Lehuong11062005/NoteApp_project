import sys
from pathlib import Path
import tkinter as tk
from tkinter import messagebox

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Frontend.controllers.auth_controller import AuthController

class ProfileWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Thông tin cá nhân")
        self.geometry("360x300")
        self.resizable(False, False)
        self.auth_controller = AuthController()

        tk.Label(self, text="👤 HỒ SƠ NGƯỜI DÙNG", font=("Arial", 14, "bold"), fg="#0288D1").pack(pady=20)

        frame_info = tk.Frame(self, padx=20)
        frame_info.pack(fill="x", expand=True)

        tk.Label(frame_info, text="Tên tài khoản:", font=("Arial", 10, "bold"), anchor="w").grid(row=0, column=0, sticky="w", pady=8)
        self.lbl_username = tk.Label(frame_info, text="...", font=("Arial", 10), fg="#333333", anchor="w")
        self.lbl_username.grid(row=0, column=1, sticky="w", padx=10, pady=8)

        tk.Label(frame_info, text="Họ và tên:", font=("Arial", 10, "bold"), anchor="w").grid(row=1, column=0, sticky="w", pady=8)
        self.lbl_fullname = tk.Label(frame_info, text="...", font=("Arial", 10), fg="#333333", anchor="w")
        self.lbl_fullname.grid(row=1, column=1, sticky="w", padx=10, pady=8)

        tk.Label(frame_info, text="Email:", font=("Arial", 10, "bold"), anchor="w").grid(row=2, column=0, sticky="w", pady=8)
        self.lbl_email = tk.Label(frame_info, text="...", font=("Arial", 10), fg="#333333", anchor="w")
        self.lbl_email.grid(row=2, column=1, sticky="w", padx=10, pady=8)

        tk.Button(self, text="Đóng", bg="#757575", fg="white", font=("Arial", 10, "bold"), width=12, command=self.destroy).pack(pady=20)

        self.load_profile()

    def load_profile(self):
        success, result = self.auth_controller.get_profile()
        if success:
            self.lbl_username.config(text=result.username)
            self.lbl_fullname.config(text=result.fullname)
            self.lbl_email.config(text=result.email if result.email else "(Chưa cập nhật)")
        else:
            messagebox.showerror("Lỗi", f"Không thể lấy thông tin: {result}", parent=self)