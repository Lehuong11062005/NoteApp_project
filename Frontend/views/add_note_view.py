import sys
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

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
        self._photo_ref = None  # giữ reference để tránh GC

        self.title("Cập nhật Ghi Chú" if self.edit_mode else "Thêm Ghi Chú Mới")
        self.geometry("520x700")
        self.grab_set()

        # Tiêu đề
        tk.Label(self, text="Tiêu đề:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_title = tk.Entry(self, width=60, font=("Arial", 10))
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
        # KHU VỰC THỜI GIAN NHẮC NHỞ (từ main - dùng DateEntry có lịch)
        # ==========================================
        self.use_reminder_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self, text="Bật nhắc nhở (Chọn ngày giờ)",
            variable=self.use_reminder_var,
            command=self.toggle_reminder
        ).pack(anchor="w", padx=5, pady=(5, 0))

        # Khung vỏ bọc cố định
        self.reminder_container = tk.Frame(self)
        self.reminder_container.pack(fill="x", padx=10, pady=2)

        # Khung chứa bộ chọn thời gian nằm bên trong vỏ bọc
        self.frame_time = tk.Frame(self.reminder_container)

        # Bộ chọn Ngày (DateEntry - có lịch popup)
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

        # Đính kèm ảnh (Upload qua API - từ feature/image-upload)
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

        # Khu vực hiển thị ảnh preview
        self.lbl_img_preview = tk.Label(frame_img_box, bg="#f0f0f0", relief="flat")

        if self.uploaded_image_url:
            self.lbl_img_status.config(text="✓ Đã có ảnh đính kèm", fg="#2E7D32")
            self._load_image_from_url(self.uploaded_image_url)
        else:
            self.btn_clear_img.pack_forget()

        # Trạng thái (Chỉ hiển thị khi đang trong chế độ Sửa)
        if self.edit_mode:
            tk.Label(self, text="Trạng thái:").pack(anchor="w", padx=10, pady=(5, 0))
            self.cb_status = ttk.Combobox(self, values=["Đang chờ", "Đã hoàn thành", "Quá hạn"], width=57)
            self.cb_status.pack(padx=10, pady=2)

            current_status = getattr(note_data, "status", "Đang chờ")
            self.cb_status.set(current_status)

        # Nội dung
        tk.Label(self, text="Nội dung:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(5, 0))
        self.txt_content = tk.Text(self, height=8, width=60, font=("Arial", 10))
        self.txt_content.pack(padx=10, pady=2)

        # Nạp dữ liệu cũ nếu là chế độ Sửa
        if self.edit_mode:
            self.entry_title.insert(0, getattr(note_data, "title", ""))
            self.cb_category.set(getattr(note_data, "category", "Chung"))
            self.cb_priority.set(getattr(note_data, "priority", "Bình Thường"))
            self.txt_content.insert("1.0", getattr(note_data, "content", ""))

            # Khôi phục thời gian nhắc nhở nếu có
            reminder = getattr(note_data, "reminder_time", "")
            if reminder and len(str(reminder)) >= 16:  # Format: YYYY-MM-DD HH:MM
                self.use_reminder_var.set(True)
                self.toggle_reminder()

                reminder_str = str(reminder)
                date_part = reminder_str[:10]
                time_part = reminder_str[11:16]
                hour_part, min_part = time_part.split(":")

                self.cal_date.set_date(date_part)
                self.spin_hour.set(hour_part)
                self.spin_minute.set(min_part)

        self.btn_save = tk.Button(
            self, text="Cập nhật" if self.edit_mode else "Lưu Ghi Chú",
            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.save_note,
            padx=15, pady=5, cursor="hand2"
        )
        self.btn_save.pack(pady=12)

    def toggle_reminder(self):
        """Hàm bật/tắt hiển thị bộ chọn thời gian an toàn trong Container"""
        if self.use_reminder_var.get():
            self.frame_time.pack(fill="x")
        else:
            self.frame_time.pack_forget()

    def _load_image_from_url(self, url: str):
        """Tải và hiển thị ảnh preview từ URL (chạy ngầm)"""
        if not PIL_AVAILABLE or not url:
            return

        def _fetch():
            try:
                import urllib.request
                import io
                with urllib.request.urlopen(url, timeout=5) as resp:
                    data = resp.read()
                img = Image.open(io.BytesIO(data))
                img.thumbnail((200, 150), Image.LANCZOS)
                self.after(0, lambda: self._show_preview(img))
            except Exception:
                pass  # Nếu không tải được thì bỏ qua

        threading.Thread(target=_fetch, daemon=True).start()

    def _show_preview(self, img):
        """Hiển thị ảnh thumbnail lên giao diện"""
        photo = ImageTk.PhotoImage(img)
        self._photo_ref = photo
        self.lbl_img_preview.config(image=photo)
        self.lbl_img_preview.pack(padx=5, pady=(0, 5))

    def _show_local_preview(self, filepath: str):
        """Hiển thị ảnh preview từ file local"""
        if not PIL_AVAILABLE:
            return
        try:
            img = Image.open(filepath)
            img.thumbnail((200, 150), Image.LANCZOS)
            self._show_preview(img)
        except Exception:
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

        # Hiển thị preview từ file local ngay lập tức
        self._show_local_preview(filepath)

        def _do_upload():
            success, res = UploadAPI.upload_image(filepath)
            self.after(0, lambda: self._on_upload_done(success, res))

        threading.Thread(target=_do_upload, daemon=True).start()

    def _on_upload_done(self, success: bool, res: str):
        self.btn_select_img.config(state="normal")
        if success:
            self.uploaded_image_url = res
            self.lbl_img_status.config(text="✓ Đã đính kèm ảnh", fg="#2E7D32")
            self.btn_clear_img.pack(side="left")
        else:
            self.lbl_img_status.config(text=f"❌ {res}", fg="#C62828")
            # Ẩn preview nếu upload thất bại
            self.lbl_img_preview.pack_forget()
            messagebox.showerror("Lỗi tải ảnh", f"Không thể upload ảnh:\n{res}")

    def on_clear_image(self):
        self.uploaded_image_url = None
        self._photo_ref = None
        self.lbl_img_status.config(text="Chưa có ảnh nào", fg="#666666")
        self.lbl_img_preview.config(image="")
        self.lbl_img_preview.pack_forget()
        self.btn_clear_img.pack_forget()

    def save_note(self):
        title = self.entry_title.get().strip()
        content = self.txt_content.get("1.0", tk.END).strip()
        category = self.cb_category.get()
        priority = self.cb_priority.get()
        image_url = self.uploaded_image_url

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
