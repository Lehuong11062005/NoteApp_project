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
        self.geometry("480x600") # Tăng chiều cao để chứa đủ các trường mới
        self.grab_set()

        # Tiêu đề
        tk.Label(self, text="Tiêu đề:").pack(anchor="w", padx=10, pady=(10,0))
        self.entry_title = tk.Entry(self, width=55)
        self.entry_title.pack(padx=10, pady=2)

        # Cụm Chủ đề & Mức độ (chia 2 cột cho gọn)
        frame_row1 = tk.Frame(self)
        frame_row1.pack(fill="x", padx=10, pady=5)
        
        tk.Label(frame_row1, text="Chủ đề:").pack(side="left")
        self.cb_category = ttk.Combobox(frame_row1, values=["Học tập", "Công việc", "Cá nhân", "Chung"], width=15)
        self.cb_category.current(3)
        self.cb_category.pack(side="left", padx=(5, 15))

        tk.Label(frame_row1, text="Mức độ:").pack(side="left")
        self.cb_priority = ttk.Combobox(frame_row1, values=["Thấp", "Bình Thường", "Cao"], width=15)
        self.cb_priority.current(1)
        self.cb_priority.pack(side="left", padx=5)

        # Thời gian nhắc nhở & Ảnh URL
        tk.Label(self, text="Thời gian nhắc (YYYY-MM-DD HH:MM) - Tùy chọn:").pack(anchor="w", padx=10, pady=(5,0))
        self.entry_reminder = tk.Entry(self, width=55)
        self.entry_reminder.pack(padx=10, pady=2)

        tk.Label(self, text="Link ảnh đính kèm (URL) - Tùy chọn:").pack(anchor="w", padx=10, pady=(5,0))
        self.entry_image = tk.Entry(self, width=55)
        self.entry_image.pack(padx=10, pady=2)

        # Trạng thái (Chỉ hiển thị khi đang trong chế độ Sửa)
        if self.edit_mode:
            tk.Label(self, text="Trạng thái:").pack(anchor="w", padx=10, pady=(5,0))
            self.cb_status = ttk.Combobox(self, values=["Đang chờ", "Đã hoàn thành", "Quá hạn"], width=52)
            self.cb_status.pack(padx=10, pady=2)
            
            # Cài đặt giá trị hiện tại
            current_status = getattr(note_data, "status", "Đang chờ")
            self.cb_status.set(current_status)

        # Nội dung
        tk.Label(self, text="Nội dung:").pack(anchor="w", padx=10, pady=(5,0))
        self.txt_content = tk.Text(self, height=10, width=55)
        self.txt_content.pack(padx=10, pady=2)

        # Nạp dữ liệu cũ nếu là chế độ Sửa
        if self.edit_mode:
            self.entry_title.insert(0, getattr(note_data, "title", ""))
            self.cb_category.set(getattr(note_data, "category", "Chung"))
            self.cb_priority.set(getattr(note_data, "priority", "Bình Thường"))
            
            reminder = getattr(note_data, "reminder_time", "")
            if reminder: self.entry_reminder.insert(0, str(reminder))
            
            image_url = getattr(note_data, "image_url", "")
            if image_url: self.entry_image.insert(0, str(image_url))
            
            self.txt_content.insert("1.0", getattr(note_data, "content", ""))

        self.btn_save = tk.Button(
            self, text="Cập nhật" if self.edit_mode else "Lưu Ghi Chú",
            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.save_note
        )
        self.btn_save.pack(pady=15)

    def save_note(self):
        title = self.entry_title.get().strip()
        content = self.txt_content.get("1.0", tk.END).strip()
        category = self.cb_category.get()
        priority = self.cb_priority.get()
        reminder_time = self.entry_reminder.get().strip() or None
        image_url = self.entry_image.get().strip() or None

        if self.edit_mode:
            status = self.cb_status.get()
            success, msg = self.note_controller.update_note(
                note_id=self.note_id, title=title, content=content,
                category=category, priority=priority,
                reminder_time=reminder_time, image_url=image_url, status=status
            )
        else:
            success, msg = self.note_controller.create_note(
                title=title, content=content, category=category, priority=priority,
                reminder_time=reminder_time, image_url=image_url
            )

        if success:
            messagebox.showinfo("Thành công", msg)
            self.destroy()
        else:
            messagebox.showerror("Lỗi", msg)