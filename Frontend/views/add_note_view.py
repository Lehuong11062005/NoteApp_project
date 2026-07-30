# frontend/views/add_note_view.py
import os
import io
import requests
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from Frontend.controllers.note_controller import NoteController
from Frontend.services.note_api import NoteAPI

class AddNoteWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = NoteController(self)
        self.title("Thêm Ghi Chú Mới")
        self.geometry("520x680")
        
        self.thumbnail_img = None  # Giữ reference tránh bị garbage collector thu hồi ảnh
        
        # Tiêu đề
        tk.Label(self, text="Tiêu đề:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10, pady=(10,0))
        self.entry_title = tk.Entry(self, width=55)
        self.entry_title.pack(padx=10, pady=5)

        # Chủ đề
        tk.Label(self, text="Chủ đề:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10)
        self.cb_category = ttk.Combobox(self, values=["Học tập", "Công việc", "Cá nhân", "Chung"])
        self.cb_category.current(3)
        self.cb_category.pack(padx=10, pady=5, fill="x")

        # Mức độ ưu tiên
        tk.Label(self, text="Mức độ ưu tiên:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10)
        self.cb_priority = ttk.Combobox(self, values=["Thấp", "Bình thường", "Cao"])
        self.cb_priority.current(1)
        self.cb_priority.pack(padx=10, pady=5, fill="x")

        # Lời nhắc nhở (reminder_time)
        tk.Label(self, text="Thời gian nhắc nhở (YYYY-MM-DD HH:MM):", font=("Arial", 9, "bold")).pack(anchor="w", padx=10)
        self.entry_reminder = tk.Entry(self, width=55)
        self.entry_reminder.pack(padx=10, pady=5)

        # Hình ảnh đính kèm (image_url / path)
        tk.Label(self, text="Hình ảnh đính kèm:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10)
        frame_img = tk.Frame(self)
        frame_img.pack(fill="x", padx=10, pady=5)
        
        self.entry_image = tk.Entry(frame_img, width=40)
        self.entry_image.pack(side="left", padx=(0,5))
        btn_browse = tk.Button(frame_img, text="📎 Chọn ảnh", bg="#0288D1", fg="white", font=("Arial", 9, "bold"), command=self.browse_image)
        btn_browse.pack(side="left")

        # Widget hiển thị Thumbnail ảnh thu nhỏ bằng Pillow
        self.lbl_thumbnail = tk.Label(self, text="[ Chưa chọn ảnh ]", bg="#E0E0E0", width=20, height=5)
        self.lbl_thumbnail.pack(padx=10, pady=5)

        # Nội dung
        tk.Label(self, text="Nội dung:", font=("Arial", 9, "bold")).pack(anchor="w", padx=10)
        self.txt_content = tk.Text(self, height=6, width=55)
        self.txt_content.pack(padx=10, pady=5)

        # Nút Lưu
        btn_save = tk.Button(self, text="💾 Lưu Ghi Chú", bg="#4CAF50", fg="white", font=("Arial", 11, "bold"), padx=15, pady=5, command=self.save_note)
        btn_save.pack(pady=15)

    def browse_image(self):
        """1. Dùng filedialog chọn ảnh từ máy tính.
           2. Gọi controller để tải ảnh lên server.
           3. Dùng Pillow load và hiển thị thumbnail ảnh thu nhỏ 100x100px.
        """
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
        )
        if not file_path:
            return

        # Gọi API Upload qua controller
        is_success, result = self.controller.upload_image(file_path)
        if not is_success:
            messagebox.showerror("Lỗi Upload", f"Không thể upload ảnh: {result}")
            return

        image_url = result
        self.entry_image.delete(0, tk.END)
        self.entry_image.insert(0, image_url)
        messagebox.showinfo("Thành công", f"Đã upload ảnh thành công!\nURL: {image_url}")

        # Dùng Pillow hiển thị thumbnail thu nhỏ 100x100px
        self.show_thumbnail(file_path, image_url)

    def show_thumbnail(self, local_path: str, image_url: str):
        """Dùng Pillow đọc ảnh (local hoặc qua URL) và render thumbnail thu nhỏ trên Label Tkinter."""
        try:
            pil_image = None
            if os.path.exists(local_path):
                pil_image = Image.open(local_path)
            elif image_url and image_url.startswith("http"):
                res = requests.get(image_url, timeout=5)
                if res.status_code == 200:
                    pil_image = Image.open(io.BytesIO(res.content))

            if pil_image:
                # Resize ảnh thành thumbnail 100x100 pixels bằng Pillow
                pil_image.thumbnail((100, 100))
                self.thumbnail_img = ImageTk.PhotoImage(pil_image)
                self.lbl_thumbnail.config(image=self.thumbnail_img, text="", width=100, height=100)
            else:
                self.lbl_thumbnail.config(text="[ Lỗi tải ảnh ]")
        except Exception as e:
            self.lbl_thumbnail.config(text=f"[ Lỗi thumbnail: {str(e)} ]")

    def save_note(self):
        title = self.entry_title.get().strip()
        content = self.txt_content.get("1.0", tk.END).strip()
        category = self.cb_category.get()
        priority = self.cb_priority.get()
        
        reminder_time = self.entry_reminder.get().strip() or None
        image_url = self.entry_image.get().strip() or None

        if not title or not content:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ Tiêu đề và Nội dung!")
            return

        success, msg = NoteAPI.create_note(
            title=title, 
            content=content, 
            category=category, 
            priority=priority,
            reminder_time=reminder_time,
            image_url=image_url
        )
        
        if success:
            messagebox.showinfo("Thành công", msg)
            self.destroy()
        else:
            messagebox.showerror("Lỗi", msg)