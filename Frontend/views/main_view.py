import tkinter as tk
from tkinter import ttk

class MainView(tk.Tk):
    """Màn hình chính của ứng dụng sau khi đăng nhập thành công."""

    def __init__(self, controller, profile_data: dict):
        """
        Args:
            controller: AuthController xử lý sự kiện (đăng xuất, ...).
            profile_data: dict thông tin user từ GET /auth/profile
                          {user_id, username, email, full_name, created_at}
        """
        super().__init__()
        self.controller = controller
        self.profile_data = profile_data

        self.title("NoteApp – Trang chính")
        self.geometry("450x300")
        self.resizable(False, False)

        self._setup_ui()

    def _setup_ui(self):
        # ── Tiêu đề chào mừng ──────────────────────────────────────────────
        username = self.profile_data.get("username", "Người dùng")
        tk.Label(
            self,
            text=f"Chào mừng, {username}! 👋",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        # ── Thông tin cá nhân ──────────────────────────────────────────────
        frame = tk.LabelFrame(self, text="Thông tin tài khoản", padx=15, pady=10)
        frame.pack(padx=30, fill="x")

        fields = [
            ("Tên đăng nhập:", self.profile_data.get("username", "N/A")),
            ("Email:", self.profile_data.get("email") or "Chưa cập nhật"),
            ("Họ và tên:", self.profile_data.get("full_name") or "Chưa cập nhật"),
        ]

        for i, (label_text, value_text) in enumerate(fields):
            tk.Label(frame, text=label_text, anchor="w", width=18).grid(
                row=i, column=0, sticky="w", pady=4
            )
            tk.Label(frame, text=value_text, anchor="w", fg="#333333").grid(
                row=i, column=1, sticky="w", pady=4
            )

        # ── Nút Đăng xuất ──────────────────────────────────────────────────
        ttk.Button(
            self,
            text="🚪  Đăng xuất",
            command=self.controller.handle_logout
        ).pack(pady=25)
