import tkinter as tk
from tkinter import ttk, messagebox
from controllers.note_controller import NoteController
from controllers.auth_controller import AuthController
from views.add_note_view import AddNoteWindow

class MainAppWindow(tk.Tk):
    def __init__(self, user, on_logout_callback):
        super().__init__()
        self.title("Smart Note - Quản lý Ghi chú")
        self.geometry("700x450")
        self.note_controller = NoteController()
        self.auth_controller = AuthController()
        self.on_logout_callback = on_logout_callback

        # Thanh tiêu đề (Header)
        tk.Label(self, text=f"👤 Xin chào: {user.fullname}", fg="gray", font=("Arial", 10, "italic")).pack(anchor="w", padx=15, pady=5)
        
        # Bảng danh sách ghi chú
        frame_list = tk.Frame(self)
        frame_list.pack(fill="both", expand=True, padx=15, pady=5)

        columns = ("title", "category", "priority", "create_at")
        self.tree = ttk.Treeview(frame_list, columns=columns, show="headings", height=12)
        self.tree.heading("title", text="Tiêu đề")
        self.tree.heading("category", text="Chủ đề")
        self.tree.heading("priority", text="Mức độ")
        self.tree.heading("create_at", text="Ngày tạo")
        
        self.tree.column("title", width=300)
        self.tree.column("category", width=100, anchor="center")
        self.tree.column("priority", width=100, anchor="center")
        self.tree.column("create_at", width=100, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Nút bấm chức năng
        frame_btn = tk.Frame(self)
        frame_btn.pack(fill="x", padx=15, pady=15)
        tk.Button(frame_btn, text="+ Thêm Ghi Chú", bg="#0288D1", fg="white", font=("Arial", 10, "bold"), command=self.open_add_note).pack(side="left")
        tk.Button(frame_btn, text="🔄 Tải lại", command=self.load_data).pack(side="left", padx=10)
        tk.Button(frame_btn, text="🚪 Đăng xuất", bg="#D32F2F", fg="white", font=("Arial", 10, "bold"), command=self.handle_logout).pack(side="right")

        # Khởi chạy tải dữ liệu
        self.load_data()

    def handle_logout(self):
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn đăng xuất không?"):
            self.auth_controller.logout()
            self.on_logout_callback()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        success, data = self.note_controller.get_notes()
        if success:
            for note in data:
                self.tree.insert("", "end", values=(note.title, note.category, note.priority, note.create_at))
        else:
            messagebox.showerror("Lỗi", data)

    def open_add_note(self):
        add_window = AddNoteWindow(self)
        self.wait_window(add_window)
        self.load_data() # Tự động load lại sau khi thêm xong