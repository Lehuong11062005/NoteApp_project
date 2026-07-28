import tkinter as tk
from tkinter import ttk, messagebox
from controllers.note_controller import NoteController

class AddNoteWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Thêm Ghi Chú Mới")
        self.geometry("450x450")
        self.grab_set()
        self.note_controller = NoteController()
        
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

        tk.Button(self, text="Lưu Ghi Chú", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.save_note).pack(pady=15)

    def save_note(self):
        success, msg = self.note_controller.create_note(
            title=self.entry_title.get().strip(),
            content=self.txt_content.get("1.0", tk.END).strip(),
            category=self.cb_category.get(),
            priority=self.cb_priority.get()
        )
        if success:
            messagebox.showinfo("Thành công", msg)
            self.destroy()
        else:
            messagebox.showerror("Lỗi", msg)