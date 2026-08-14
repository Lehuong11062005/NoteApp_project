import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Frontend.controllers.auth_controller import AuthController
from Frontend.controllers.note_controller import NoteController
from Frontend.views.profile_view import ProfileWindow
from Frontend.views.tabs.notes_tab import NotesTab
from Frontend.views.tabs.stats_tab import StatsTab
from Frontend.utils import image_cache

class MainAppWindow(tk.Tk):
    def __init__(self, user, on_logout_callback=None):
        super().__init__()
        self.title("Smart Note - Quản lý Ghi chú")
        self.geometry("860x650") 
        self.configure(bg="#F5F7FB")
        self.resizable(False, False)

        self.user = user
        self.on_logout_callback = on_logout_callback
        
        self.auth_controller = AuthController()
        self.note_controller = NoteController()

        self._configure_styles()
        self._build_header()
        self._build_tabs()

        # Giải phóng cache khi đóng cửa sổ (nhấn X)
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        # Load dữ liệu lần đầu
        self.notes_tab.load_data()
        self.stats_tab.load_statistics()

    def _configure_styles(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        style.configure("Treeview.Heading", background="#1976D2", foreground="white", font=("Arial", 10, "bold"))
        style.configure("Treeview", rowheight=28, font=("Arial", 10), fieldbackground="#F7FAFF", background="#FFFFFF", bordercolor="#E0E0E0", relief="flat")
        style.map("Treeview", background=[("selected", "#BBDEFB")], foreground=[("selected", "black")])

    def _build_header(self):
        header_frame = tk.Frame(self, bg="#ffffff", bd=0, relief="flat")
        header_frame.pack(fill="x", padx=15, pady=(10, 5))

        # 1. Logo / Tiêu đề
        tk.Label(header_frame, text="Smart Note", fg="#2E3A59", bg="#ffffff", font=("Arial", 16, "bold")).pack(side="left")

        # 2. Nút Đăng xuất (Góc ngoài cùng bên phải)
        tk.Button(
            header_frame, text="🚪 Đăng xuất", fg="#D32F2F", bg="#ffffff", font=("Arial", 9, "bold"), 
            bd=0, cursor="hand2", command=self.handle_logout
        ).pack(side="right", padx=(5, 0))

        # 3. Nút Hồ sơ
        tk.Button(
            header_frame, text="👤 Hồ sơ", fg="#0288D1", bg="#ffffff", font=("Arial", 9, "bold"), 
            bd=0, cursor="hand2", command=lambda: ProfileWindow(self)
        ).pack(side="right", padx=5)

        # 4. Nút Trợ lý AI (Bắt buộc hiển thị)
        btn_ai = tk.Button(
            header_frame, text="🤖 Trợ lý AI", fg="#00897B", bg="#E0F2F1", font=("Arial", 9, "bold"), 
            bd=0, cursor="hand2", padx=8, pady=2, command=self.open_chatbot
        )
        btn_ai.pack(side="right", padx=5)

        # 5. Tên người dùng
        fullname = getattr(self.user, "fullname", "Người dùng")
        tk.Label(header_frame, text=f"👤 Xin chào: {fullname}", fg="#666666", bg="#ffffff", font=("Arial", 10, "italic")).pack(side="right", padx=10)

    def open_chatbot(self):
        """Hàm mở cửa sổ Chatbot"""
        try:
            from Frontend.views.chat_window import ChatbotWindow
            user_id = getattr(self.user, "id", getattr(self.user, "_id", "guest"))
            ChatbotWindow(self, user_id=str(user_id))
        except ImportError as e:
            messagebox.showerror(
                "Lỗi File", 
                f"Chưa tìm thấy file 'Frontend/views/chat_window.py'!\nChi tiết lỗi: {e}"
            )
    def _build_tabs(self):
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=15, pady=5)

        self.notes_tab = NotesTab(notebook, self, self.note_controller)
        self.stats_tab = StatsTab(notebook, self.note_controller)

        notebook.add(self.notes_tab, text="Danh sách ghi chú")
        notebook.add(self.stats_tab, text="Thống kê")

    def _on_close(self):
        """Xử lý khi đóng cửa sổ bằng nút X."""
        image_cache.clear()
        self.destroy()
        if self.on_logout_callback:
            self.on_logout_callback()

    def handle_logout(self):
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất?"):
            self.auth_controller.logout()
            image_cache.clear()
            self.destroy()
            if self.on_logout_callback:
                self.on_logout_callback()