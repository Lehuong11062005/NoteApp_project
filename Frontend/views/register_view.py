import tkinter as tk
from tkinter import ttk
from controllers.auth_controller import AuthController

class RegisterView(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Đăng ký tài khoản - NoteApp")
        self.geometry("380x320")
        self.resizable(False, False)

        # Khởi tạo controller
        self.controller = AuthController(self)
        self._setup_ui()

    def _setup_ui(self):
        # Tiêu đề
        tk.Label(self, text="ĐĂNG KÝ TÀI KHOẢN", font=("Arial", 14, "bold")).pack(pady=15)

        # Form nhập liệu
        frame = tk.Frame(self)
        frame.pack(padx=20, fill="x")

        # Username
        tk.Label(frame, text="Tài khoản (*):").grid(row=0, column=0, sticky="w", pady=5)
        self.entry_username = ttk.Entry(frame, width=30)
        self.entry_username.grid(row=0, column=1, pady=5, padx=5)

        # Password
        tk.Label(frame, text="Mật khẩu (*):").grid(row=1, column=0, sticky="w", pady=5)
        self.entry_password = ttk.Entry(frame, width=30, show="*")
        self.entry_password.grid(row=1, column=1, pady=5, padx=5)

        # Email
        tk.Label(frame, text="Email:").grid(row=2, column=0, sticky="w", pady=5)
        self.entry_email = ttk.Entry(frame, width=30)
        self.entry_email.grid(row=2, column=1, pady=5, padx=5)

        # Fullname
        tk.Label(frame, text="Họ và tên:").grid(row=3, column=0, sticky="w", pady=5)
        self.entry_fullname = ttk.Entry(frame, width=30)
        self.entry_fullname.grid(row=3, column=1, pady=5, padx=5)

        # Nút chức năng
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=20)

        ttk.Button(btn_frame, text="Thoát", command=self.destroy).pack(side="left", padx=15)
        ttk.Button(btn_frame, text="Xác nhận Đăng ký", command=self._on_register_click).pack(side="left", padx=15)
        
        # Bắt sự kiện phím Enter khi đang gõ trong form
        self.bind('<Return>', lambda event: self._on_register_click())

    def _on_register_click(self):
        """Kích hoạt hàm đăng ký ở Controller"""
        self.controller.handle_register()

    # --- HÀM BỔ SUNG: Giúp Controller lấy dữ liệu sạch sẽ ---
    def get_register_data(self) -> dict:
        """Trả về dữ liệu người dùng nhập dưới dạng dictionary"""
        return {
            "username": self.entry_username.get().strip(),
            "password": self.entry_password.get(),  # Giữ nguyên chuỗi mật khẩu gốc (không mã hóa ở đây)
            "email": self.entry_email.get().strip(),
            "full_name": self.entry_fullname.get().strip()
        }