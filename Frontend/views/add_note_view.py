import os
import io
import requests
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from PIL import Image, ImageTk
from controllers.note_controller import NoteController

class AddNoteWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.controller = NoteController(self)
        self.title("Thêm Ghi Chú Mới")
        self.geometry("450x600")
        self.grab_set()

        self.thumbnail_img = None  # Giữ reference tránh bị garbage collector thu hồi ảnh

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

        # Hình ảnh đính kèm — tính năng mới từ image-upload
        tk.Label(self, text="Hình ảnh đính kèm:").pack(anchor="w", padx=10)
        frame_img = tk.Frame(self)
        frame_img.pack(fill="x", padx=10, pady=5)

        self.entry_image = tk.Entry(frame_img, width=35)
        self.entry_image.pack(side="left", padx=(0, 5))
        btn_browse = tk.Button(frame_img, text="📎 Chọn ảnh", bg="#0288D1", fg="white",
                               font=("Arial", 9, "bold"), command=self.browse_image)
        btn_browse.pack(side="left")

        # Thumbnail ảnh thu nhỏ bằng Pillow
        self.lbl_thumbnail = tk.Label(self, text="[ Chưa chọn ảnh ]", bg="#E0E0E0", width=20, height=5)
        self.lbl_thumbnail.pack(padx=10, pady=5)

        tk.Label(self, text="Nội dung:").pack(anchor="w", padx=10)
        self.txt_content = tk.Text(self, height=8, width=50)
        self.txt_content.pack(padx=10, pady=5)

        tk.Button(self, text="Lưu Ghi Chú", bg="#4CAF50", fg="white",
                  font=("Arial", 10, "bold"), command=self.save_note).pack(pady=15)

    def browse_image(self):
        """Chọn ảnh, upload lên ImgBB qua controller, hiển thị thumbnail."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Image files", "*.png *.jpg *.jpeg"), ("All files", "*.*")]
        )
        if not file_path:
            return

        is_success, result = self.controller.upload_image(file_path)
        if not is_success:
            messagebox.showerror("Lỗi Upload", f"Không thể upload ảnh: {result}")
            return

        image_url = result
        self.entry_image.delete(0, tk.END)
        self.entry_image.insert(0, image_url)
        messagebox.showinfo("Thành công", f"Đã upload ảnh!\nURL: {image_url}")
        self.show_thumbnail(file_path, image_url)

    def show_thumbnail(self, local_path: str, image_url: str):
        """Dùng Pillow đọc ảnh local và render thumbnail 100x100 px."""
        try:
            pil_image = None
            if os.path.exists(local_path):
                pil_image = Image.open(local_path)
            elif image_url and image_url.startswith("http"):
                res = requests.get(image_url, timeout=5)
                if res.status_code == 200:
                    pil_image = Image.open(io.BytesIO(res.content))

            if pil_image:
                pil_image.thumbnail((100, 100))
                self.thumbnail_img = ImageTk.PhotoImage(pil_image)
                self.lbl_thumbnail.config(image=self.thumbnail_img, text="", width=100, height=100)
            else:
                self.lbl_thumbnail.config(text="[ Lỗi tải ảnh ]")
        except Exception as e:
            self.lbl_thumbnail.config(text=f"[ Lỗi thumbnail: {str(e)} ]")

    def save_note(self):
        image_url = self.entry_image.get().strip() or None
        success, msg = self.controller.create_note(
            title=self.entry_title.get().strip(),
            content=self.txt_content.get("1.0", tk.END).strip(),
            category=self.cb_category.get(),
            priority=self.cb_priority.get(),
            image_url=image_url
        )
        if success:
            messagebox.showinfo("Thành công", msg)
            self.destroy()
        else:
            messagebox.showerror("Lỗi", msg)