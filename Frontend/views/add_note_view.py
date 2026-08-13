import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry 

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
        self.geometry("500x650")
        self.grab_set()

        # Tiêu đề
        tk.Label(self, text="Tiêu đề:").pack(anchor="w", padx=10, pady=(10,0))
        self.entry_title = tk.Entry(self, width=55)
        self.entry_title.pack(padx=10, pady=2)

        # Cụm Chủ đề & Mức độ
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

        # ==========================================
        # KHU VỰC THỜI GIAN NHẮC NHỞ (CÓ CONTAINER GIỮ CHỖ)
        # ==========================================
        self.use_reminder_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self, text="Bật nhắc nhở (Chọn ngày giờ)", 
            variable=self.use_reminder_var, 
            command=self.toggle_reminder
        ).pack(anchor="w", padx=5, pady=(5,0))

        # Khung vỏ bọc cố định
        self.reminder_container = tk.Frame(self)
        self.reminder_container.pack(fill="x", padx=10, pady=2)

        # Khung chứa bộ chọn thời gian nằm bên trong vỏ bọc
        self.frame_time = tk.Frame(self.reminder_container)

        # Bộ chọn Ngày
        self.cal_date = DateEntry(
            self.frame_time, width=12, background='#1976D2',
            foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd'
        )
        self.cal_date.pack(side="left", padx=(0, 15))

        # Bộ chọn Giờ
        tk.Label(self.frame_time, text="Giờ:").pack(side="left")
        self.spin_hour = ttk.Spinbox(self.frame_time, from_=0, to=23, width=3, format="%02.0f")
        self.spin_hour.set("08")
        self.spin_hour.pack(side="left", padx=(2, 10))

        # Bộ chọn Phút
        tk.Label(self.frame_time, text="Phút:").pack(side="left")
        self.spin_minute = ttk.Spinbox(self.frame_time, from_=0, to=59, width=3, format="%02.0f")
        self.spin_minute.set("00")
        self.spin_minute.pack(side="left", padx=(2, 0))

        self.toggle_reminder()
        # ==========================================

        # Link ảnh đính kèm
        tk.Label(self, text="Link ảnh đính kèm (URL) - Tùy chọn:").pack(anchor="w", padx=10, pady=(10,0))
        self.entry_image = tk.Entry(self, width=55)
        self.entry_image.pack(padx=10, pady=2)

        # Trạng thái (Chỉ hiển thị khi đang trong chế độ Sửa)
        if self.edit_mode:
            tk.Label(self, text="Trạng thái:").pack(anchor="w", padx=10, pady=(5,0))
            self.cb_status = ttk.Combobox(self, values=["Đang chờ", "Đã hoàn thành", "Quá hạn"], width=52)
            self.cb_status.pack(padx=10, pady=2)
            
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
            self.txt_content.insert("1.0", getattr(note_data, "content", ""))
            
            image_url = getattr(note_data, "image_url", "")
            if image_url: self.entry_image.insert(0, str(image_url))
            
            # Khôi phục thời gian nhắc nhở nếu có
            reminder = getattr(note_data, "reminder_time", "")
            if reminder and len(reminder) >= 16: # Format: YYYY-MM-DD HH:MM
                self.use_reminder_var.set(True)
                self.toggle_reminder()
                
                date_part, time_part = reminder.split(" ")
                hour_part, min_part = time_part.split(":")
                
                self.cal_date.set_date(date_part)
                self.spin_hour.set(hour_part)
                self.spin_minute.set(min_part)

        self.btn_save = tk.Button(
            self, text="Cập nhật" if self.edit_mode else "Lưu Ghi Chú",
            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.save_note
        )
        self.btn_save.pack(pady=15)

    def toggle_reminder(self):
        """Hàm bật/tắt hiển thị bộ chọn thời gian an toàn trong Container"""
        if self.use_reminder_var.get():
            self.frame_time.pack(fill="x")
        else:
            self.frame_time.pack_forget()

    def save_note(self):
        title = self.entry_title.get().strip()
        content = self.txt_content.get("1.0", tk.END).strip()
        category = self.cb_category.get()
        priority = self.cb_priority.get()
        image_url = self.entry_image.get().strip() or None
        
        # Lấy dữ liệu thời gian nếu Checkbox được bật
        reminder_time = None
        if self.use_reminder_var.get():
            date_val = self.cal_date.get()
            hour_val = self.spin_hour.get().zfill(2)
            minute_val = self.spin_minute.get().zfill(2)
            reminder_time = f"{date_val} {hour_val}:{minute_val}"

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