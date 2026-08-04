import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Frontend.controllers.note_controller import NoteController

class AddNoteWindow(tk.Toplevel):
    def __init__(self, parent, note_data=None):
        super().__init__(parent)
        self.note_controller = NoteController()
        self.note_data = note_data
        self.note_id = getattr(note_data, "id", None) if note_data else None
        self.edit_mode = self.note_id is not None

        self.title("Cập nhật Ghi Chú" if self.edit_mode else "Thêm Ghi Chú Mới")
        self.geometry("450x450")
        self.grab_set()

        username = getattr(getattr(parent, "note_controller", None), "username", None)
        self.note_controller = NoteController(username)

        tk.Label(self, text="Tiêu đề:").pack(anchor="w", padx=10, pady=(10,0))
        self.entry_title = tk.Entry(self, width=50)
        self.entry_title.pack(padx=10, pady=5)

        tk.Label(self, text="Chủ đề:").pack(anchor="w", padx=10)
        self.cb_category = ttk.Combobox(self, values=["Học tập", "Công việc", "Cá nhân", "Chung"])
        self.cb_category.current(3)
        self.cb_category.pack(padx=10, pady=5, fill="x")

        tk.Label(self, text="Mức độ:").pack(anchor="w", padx=10)
        self.cb_priority = ttk.Combobox(self, values=["Thấp", "Bình thường", "Cao"])
        self.cb_priority.current(1)
        self.cb_priority.pack(padx=10, pady=5, fill="x")

        tk.Label(self, text="Nội dung:").pack(anchor="w", padx=10)
        self.txt_content = tk.Text(self, height=8, width=50)
        self.txt_content.pack(padx=10, pady=5)

        if self.edit_mode:
            self.entry_title.insert(0, getattr(note_data, "title", ""))
            self.cb_category.set(getattr(note_data, "category", "Chung"))
            self.cb_priority.set(getattr(note_data, "priority", "Bình thường"))
            self.txt_content.insert("1.0", getattr(note_data, "content", ""))

        self.btn_save = tk.Button(
            self,
            text="Cập nhật" if self.edit_mode else "Lưu Ghi Chú",
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            command=self.save_note
        )
        self.btn_save.pack(pady=15)

    def save_note(self):
        title = self.entry_title.get().strip()
        content = self.txt_content.get("1.0", tk.END).strip()
        category = self.cb_category.get()
        priority = self.cb_priority.get()

        if self.edit_mode:
            success, msg = self.note_controller.update_note(
                note_id=self.note_id,
                title=title,
                content=content,
                category=category,
                priority=priority
            )
        else:
            success, msg = self.note_controller.create_note(
                title=title,
                content=content,
                category=category,
                priority=priority
            )

        if success:
            messagebox.showinfo("Thành công", msg)
            self.destroy()
        else:
            messagebox.showerror("Lỗi", msg)
    def save_note(self):
        title = self.entry_title.get().strip()
        content = self.txt_content.get("1.0", tk.END).strip()
        category = self.cb_category.get()
        priority = self.cb_priority.get()

        if self.edit_mode:
            success, msg = self.note_controller.update_note(
                note_id=self.note_id,
                title=title,
                content=content,
                category=category,
                priority=priority
            )
        else:
            success, msg = self.note_controller.create_note(
                title=title,
                content=content,
                category=category,
                priority=priority
            )

        if success:
            messagebox.showinfo("Thành công", msg)
            self.destroy()
        else:
            messagebox.showerror("Lỗi", msg)