import sys
import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Frontend.controllers.note_controller import NoteController
from Frontend.utils.file_helper import choose_image_file
from Frontend.services.upload_api import UploadAPI

class AddNoteWindow(tk.Toplevel):
    def __init__(self, parent, note_data=None):
        super().__init__(parent)
        self.note_controller = NoteController() 
        self.note_data = note_data
        self.note_id = getattr(note_data, "id", None) if note_data else None
        self.edit_mode = self.note_id is not None
        self.uploaded_image_url = getattr(note_data, "image_url", None) if self.edit_mode else None

        self.title("Cập nhật Ghi Chú" if self.edit_mode else "Thêm Ghi Chú Mới")
        self.geometry("520x680")

        # Tiêu đề
        tk.Label(self, text="Tiêu đề:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        self.entry_title = tk.Entry(self, width=60, font=("Arial", 10))
        self.entry_title.pack(padx=10, pady=2)

        # Cụm Chủ đề & Mức độ (chia 2 cột)
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

        # Thời gian nhắc nhở (Giao diện chọn Ngày/Tháng/Năm Giờ:Phút)
        frame_reminder_box = tk.LabelFrame(self, text="Hẹn giờ nhắc nhở (Tùy chọn)", font=("Arial", 9, "bold"), fg="#333333")
        frame_reminder_box.pack(fill="x", padx=10, pady=5)

        self.var_enable_reminder = tk.BooleanVar(value=False)
        self.chk_reminder = tk.Checkbutton(
            frame_reminder_box, text="Bật nhắc nhở", variable=self.var_enable_reminder,
            command=self._toggle_reminder_state, font=("Arial", 9)
        )
        self.chk_reminder.pack(anchor="w", padx=5, pady=2)

        frame_datetime = tk.Frame(frame_reminder_box)
        frame_datetime.pack(fill="x", padx=5, pady=2)

        now = datetime.datetime.now()
        
        tk.Label(frame_datetime, text="Ngày:").pack(side="left")
        self.sb_day = ttk.Spinbox(frame_datetime, from_=1, to=31, width=4, format="%02.0f")
        self.sb_day.pack(side="left", padx=(2, 6))
        self.sb_day.set(f"{now.day:02d}")

        tk.Label(frame_datetime, text="Tháng:").pack(side="left")
        self.sb_month = ttk.Spinbox(frame_datetime, from_=1, to=12, width=4, format="%02.0f")
        self.sb_month.pack(side="left", padx=(2, 6))
        self.sb_month.set(f"{now.month:02d}")

        tk.Label(frame_datetime, text="Năm:").pack(side="left")
        self.sb_year = ttk.Spinbox(frame_datetime, from_=2024, to=2035, width=6)
        self.sb_year.pack(side="left", padx=(2, 10))
        self.sb_year.set(str(now.year))

        tk.Label(frame_datetime, text="Giờ:").pack(side="left")
        self.sb_hour = ttk.Spinbox(frame_datetime, from_=0, to=23, width=4, format="%02.0f")
        self.sb_hour.pack(side="left", padx=(2, 6))
        self.sb_hour.set(f"{now.hour:02d}")

        tk.Label(frame_datetime, text="Phút:").pack(side="left")
        self.sb_minute = ttk.Spinbox(frame_datetime, from_=0, to=59, width=4, format="%02.0f")
        self.sb_minute.pack(side="left", padx=2)
        self.sb_minute.set(f"{now.minute:02d}")

        self.datetime_widgets = [self.sb_day, self.sb_month, self.sb_year, self.sb_hour, self.sb_minute]

        # Đính kèm ảnh (Tải lên qua API)
        frame_img_box = tk.LabelFrame(self, text="Ảnh đính kèm", font=("Arial", 9, "bold"), fg="#333333")
        frame_img_box.pack(fill="x", padx=10, pady=5)

        frame_img_actions = tk.Frame(frame_img_box)
        frame_img_actions.pack(fill="x", padx=5, pady=2)

        self.btn_select_img = tk.Button(
            frame_img_actions, text="📷 Chọn ảnh...", bg="#1976D2", fg="white",
            font=("Arial", 9, "bold"), relief="flat", cursor="hand2", command=self.on_choose_image
        )
        self.btn_select_img.pack(side="left", padx=(0, 10))

        self.btn_clear_img = tk.Button(
            frame_img_actions, text="❌ Xóa ảnh", bg="#E53935", fg="white",
            font=("Arial", 9), relief="flat", cursor="hand2", command=self.on_clear_image
        )
        self.btn_clear_img.pack(side="left")

        self.lbl_img_status = tk.Label(frame_img_box, text="Chưa có ảnh nào", fg="#666666", anchor="w", wraplength=480)
        self.lbl_img_status.pack(fill="x", padx=5, pady=(2, 5))

        if self.uploaded_image_url:
            self.lbl_img_status.config(text=f"✓ Đã có ảnh đính kèm", fg="#2E7D32")
        else:
            self.btn_clear_img.pack_forget()

        # Trạng thái (Chỉ hiển thị khi đang trong chế độ Sửa)
        if self.edit_mode:
            tk.Label(self, text="Trạng thái:").pack(anchor="w", padx=10, pady=(5,0))
            self.cb_status = ttk.Combobox(self, values=["Đang chờ", "Đã hoàn thành", "Quá hạn"], width=57)
            self.cb_status.pack(padx=10, pady=2)
            
            current_status = getattr(note_data, "status", "Đang chờ")
            self.cb_status.set(current_status)

        # Nội dung
        tk.Label(self, text="Nội dung:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(5,0))
        self.txt_content = tk.Text(self, height=8, width=60, font=("Arial", 10))
        self.txt_content.pack(padx=10, pady=2)

        # Nạp dữ liệu cũ nếu là chế độ Sửa
        if self.edit_mode:
            self.entry_title.insert(0, getattr(note_data, "title", ""))
            self.cb_category.set(getattr(note_data, "category", "Chung"))
            self.cb_priority.set(getattr(note_data, "priority", "Bình Thường"))
            
            reminder = getattr(note_data, "reminder_time", "")
            if reminder:
                self._load_reminder_time(str(reminder))
            
            self.txt_content.insert("1.0", getattr(note_data, "content", ""))

        self._toggle_reminder_state()

        self.btn_save = tk.Button(
            self, text="Cập nhật" if self.edit_mode else "Lưu Ghi Chú",
            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.save_note,
            padx=15, pady=5, cursor="hand2"
        )
        self.btn_save.pack(pady=12)

    def _toggle_reminder_state(self):
        state = "normal" if self.var_enable_reminder.get() else "disabled"
        for w in self.datetime_widgets:
            w.config(state=state)

    def _load_reminder_time(self, reminder_str: str):
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M"):
            try:
                dt = datetime.datetime.strptime(reminder_str.strip(), fmt)
                self.var_enable_reminder.set(True)
                self.sb_day.set(f"{dt.day:02d}")
                self.sb_month.set(f"{dt.month:02d}")
                self.sb_year.set(str(dt.year))
                self.sb_hour.set(f"{dt.hour:02d}")
                self.sb_minute.set(f"{dt.minute:02d}")
                return
            except ValueError:
                pass

    def on_choose_image(self):
        filepath = choose_image_file()
        if not filepath:
            return

        import os
        filename = os.path.basename(filepath)
        self.lbl_img_status.config(text=f"⏳ Đang tải '{filename}' lên...", fg="#E65100")
        self.btn_select_img.config(state="disabled")
        self.update_idletasks()

        def _do_upload():
            success, res = UploadAPI.upload_image(filepath)
            self.after(0, lambda: self._on_upload_done(success, res))

        import threading
        threading.Thread(target=_do_upload, daemon=True).start()

    def _on_upload_done(self, success: bool, res: str):
        self.btn_select_img.config(state="normal")
        if success:
            self.uploaded_image_url = res
            self.lbl_img_status.config(text="✓ Đã đính kèm ảnh", fg="#2E7D32")
            self.btn_clear_img.pack(side="left")
        else:
            self.lbl_img_status.config(text=f"❌ {res}", fg="#C62828")
            messagebox.showerror("Lỗi tải ảnh", f"Không thể upload ảnh:\n{res}")

    def on_clear_image(self):
        self.uploaded_image_url = None
        self.lbl_img_status.config(text="Chưa có ảnh nào", fg="#666666")
        self.btn_clear_img.pack_forget()

    def save_note(self):
        title = self.entry_title.get().strip()
        content = self.txt_content.get("1.0", tk.END).strip()
        category = self.cb_category.get()
        priority = self.cb_priority.get()
        image_url = self.uploaded_image_url

        reminder_time = None
        if self.var_enable_reminder.get():
            try:
                d = int(self.sb_day.get())
                m = int(self.sb_month.get())
                y = int(self.sb_year.get())
                h = int(self.sb_hour.get())
                mn = int(self.sb_minute.get())
                reminder_time = f"{y:04d}-{m:02d}-{d:02d} {h:02d}:{mn:02d}"
            except ValueError:
                messagebox.showerror("Lỗi", "Ngày giờ nhắc nhở không hợp lệ!")
                return

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