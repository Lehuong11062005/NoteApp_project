import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Frontend.controllers.note_controller import NoteController
from Frontend.controllers.auth_controller import AuthController
from Frontend.views.add_note_view import AddNoteWindow
from Frontend.views.profile_view import ProfileWindow


class MainAppWindow(tk.Tk):
    def __init__(self, user, on_logout_callback=None):
        super().__init__()
        self.title("Smart Note - Quản lý Ghi chú")
        self.geometry("700x450")
        
        # Kết hợp khởi tạo controller và xử lý user_id/username từ nhánh HEAD
        self.note_controller = NoteController(user.username if hasattr(user, "username") else None)
        self.auth_controller = AuthController()
        self.on_logout_callback = on_logout_callback

        frame_header = tk.Frame(self)
        frame_header.pack(fill="x", padx=15, pady=5)
        
        tk.Label(frame_header, text=f"👤 Xin chào: {user.fullname}", fg="gray", font=("Arial", 10, "italic")).pack(side="left")
        tk.Button(frame_header, text="🚪 Đăng xuất", fg="red", font=("Arial", 9, "bold"), command=self.handle_logout).pack(side="right", padx=5)
        tk.Button(frame_header, text="👤 Hồ sơ", fg="#0288D1", font=("Arial", 9, "bold"), command=self.open_profile).pack(side="right")
        
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
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.frame_form = tk.Frame(self)

        tk.Label(self.frame_form, text="Tiêu đề:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.entry_title = tk.Entry(self.frame_form, width=40)
        self.entry_title.grid(row=0, column=1, sticky="w", padx=5, pady=2)

        tk.Label(self.frame_form, text="Chủ đề:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.cb_category = ttk.Combobox(self.frame_form, values=["Học tập", "Công việc", "Cá nhân", "Chung"], width=20)
        self.cb_category.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        self.cb_category.current(3)

        tk.Label(self.frame_form, text="Mức độ:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.cb_priority = ttk.Combobox(self.frame_form, values=["Thấp", "Bình thường", "Cao"], width=20)
        self.cb_priority.grid(row=1, column=3, sticky="w", padx=5, pady=2)
        self.cb_priority.current(1)

        tk.Label(self.frame_form, text="Nội dung:").grid(row=2, column=0, sticky="nw", padx=5, pady=2)
        self.txt_content = tk.Text(self.frame_form, height=6, width=65)
        self.txt_content.grid(row=2, column=1, columnspan=3, padx=5, pady=2)

        self.btn_update = tk.Button(self.frame_form, text="Cập nhật", bg="#FFC107", fg="black", font=("Arial", 10, "bold"), command=self.update_note)
        self.btn_update.grid(row=3, column=1, sticky="w", padx=5, pady=10)

        frame_btn = tk.Frame(self)
        frame_btn.pack(fill="x", padx=15, pady=15)
        tk.Button(frame_btn, text="+ Thêm Ghi Chú", bg="#0288D1", fg="white", font=("Arial", 10, "bold"), command=self.open_add_note).pack(side="left")
        tk.Button(frame_btn, text="🔄 Tải lại", command=self.load_data).pack(side="left", padx=10)

        # Khởi chạy tải dữ liệu
        self.selected_note_id = None
        self.notes_by_id = {}
        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        self.notes_by_id.clear()
        self.hide_update_form()
            
        success, data = self.note_controller.get_notes()
        if success:
            for note in data:
                self.notes_by_id[note.id] = note
                self.tree.insert("", "end", iid=note.id, values=(note.title, note.category, note.priority, note.create_at))
        else:
            messagebox.showerror("Lỗi", data)

    def open_add_note(self):
        add_window = AddNoteWindow(self)
        self.wait_window(add_window)
        self.load_data() 
    def open_profile(self):
        ProfileWindow(self)

    def on_tree_select(self, event):
        selected_items = self.tree.selection()
        if not selected_items:
            return
        note_id = selected_items[0]
        note = self.notes_by_id.get(note_id)
        if not note:
            return

        self.selected_note_id = note.id
        self.entry_title.delete(0, tk.END)
        self.entry_title.insert(0, note.title)
        self.cb_category.set(note.category or "Chung")
        self.cb_priority.set(note.priority or "Bình thường")
        self.txt_content.delete("1.0", tk.END)
        self.txt_content.insert(tk.END, note.content or "")
        self.show_update_form()

    def show_update_form(self):
        self.frame_form.pack(fill="x", padx=15, pady=5)

    def hide_update_form(self):
        self.frame_form.pack_forget()

    def update_note(self):
        if not self.selected_note_id:
            messagebox.showwarning("Lỗi", "Vui lòng chọn một ghi chú để cập nhật")
            return

        title = self.entry_title.get().strip()
        content = self.txt_content.get("1.0", tk.END).strip()
        category = self.cb_category.get() or "Chung"
        priority = self.cb_priority.get() or "Bình thường"

        success, msg = self.note_controller.update_note(
            note_id=self.selected_note_id,
            title=title,
            content=content,
            category=category,
            priority=priority,
        )
        if success:
            messagebox.showinfo("Thành công", msg)
            self.load_data()
            self.clear_update_form()
        else:
            messagebox.showerror("Lỗi", msg)

    def clear_update_form(self):
        self.selected_note_id = None
        self.entry_title.delete(0, tk.END)
        self.cb_category.set("Chung")
        self.cb_priority.set("Bình thường")
        self.txt_content.delete("1.0", tk.END)

    def handle_logout(self):
        if messagebox.askyesno("Đăng xuất", "Bạn có chắc chắn muốn đăng xuất?"):
            self.auth_controller.logout()
            self.destroy()
            if self.on_logout_callback:
                self.on_logout_callback()