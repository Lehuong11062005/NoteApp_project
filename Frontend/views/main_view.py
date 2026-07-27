import tkinter as tk
from tkinter import ttk
from Frontend.views.add_note_view import AddNoteWindow

class MainView(tk.Tk):
    """Màn hình chính Main App sau khi Đăng nhập thành công."""

    def __init__(self, controller, profile_data: dict):
        super().__init__()
        self.controller = controller
        self.profile_data = profile_data or {}

        self.title("NoteApp – Ứng dụng Ghi chú Cá nhân")
        self.geometry("500x380")
        self.resizable(False, False)

        self._setup_ui()

    def _setup_ui(self):
        username = self.profile_data.get("username", "Người dùng")
        
        # Header chào mừng
        header_frame = tk.Frame(self, bg="#0288D1", padding=10)
        header_frame.pack(fill="x")
        
        tk.Label(
            header_frame,
            text=f"👋 Chào mừng, {username}!",
            font=("Arial", 14, "bold"),
            bg="#0288D1",
            fg="white"
        ).pack(anchor="w", padx=10, pady=5)

        # Thông tin user (Profile)
        frame_profile = tk.LabelFrame(self, text="Thông tin tài khoản (Profile)", padx=15, pady=10)
        frame_profile.pack(padx=20, pady=15, fill="x")

        fields = [
            ("User ID:", self.profile_data.get("user_id", "N/A")),
            ("Tên đăng nhập:", self.profile_data.get("username", "N/A")),
            ("Email:", self.profile_data.get("email") or "Chưa cập nhật"),
            ("Họ và tên:", self.profile_data.get("full_name") or "Chưa cập nhật"),
        ]

        for i, (label_text, value_text) in enumerate(fields):
            tk.Label(frame_profile, text=label_text, anchor="w", font=("Arial", 9, "bold"), width=16).grid(
                row=i, column=0, sticky="w", pady=3
            )
            tk.Label(frame_profile, text=value_text, anchor="w", fg="#333333", font=("Arial", 9)).grid(
                row=i, column=1, sticky="w", pady=3
            )

        # Action Buttons Frame
        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        # Nút Mở cửa sổ Thêm Ghi Chú
        btn_add_note = tk.Button(
            btn_frame,
            text="+ Thêm Ghi Chú Mới",
            bg="#2E7D32",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=6,
            command=self.open_add_note
        )
        btn_add_note.pack(side="left", padx=10)

        # Nút Đăng Xuất (Xóa token, quay lại Login)
        btn_logout = tk.Button(
            btn_frame,
            text="🚪 Đăng xuất",
            bg="#D32F2F",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=12,
            pady=6,
            command=self.controller.handle_logout
        )
        btn_logout.pack(side="left", padx=10)

    def open_add_note(self):
        """Mở cửa sổ Thêm ghi chú mới"""
        add_window = AddNoteWindow(self)
        add_window.grab_set()
