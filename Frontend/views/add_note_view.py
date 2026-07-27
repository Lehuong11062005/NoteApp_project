# frontend/views/add_note_view.py
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from Frontend.services.note_api import NoteAPI
class AddNoteWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Thêm Ghi Chú Mới")
        self.geometry("480x550")
        
        # Tiêu đề
        tk.Label(self, text="Tiêu đề:").pack(anchor="w", padx=10, pady=(10,0))
        self.entry_title = tk.Entry(self, width=50)
        self.entry_title.pack(padx=10, pady=5)

        # Chủ đề
        tk.Label(self, text="Chủ đề:").pack(anchor="w", padx=10)
        self.cb_category = ttk.Combobox(self, values=["Học tập", "Công việc", "Cá nhân", "Chung"])
        self.cb_category.current(3)
        self.cb_category.pack(padx=10, pady=5, fill="x")

        # Mức độ ưu tiên
        tk.Label(self, text="Mức độ ưu tiên:").pack(anchor="w", padx=10)
        self.cb_priority = ttk.Combobox(self, values=["Thấp", "Bình thường", "Cao"])
        self.cb_priority.current(1)
        self.cb_priority.pack(padx=10, pady=5, fill="x")

        # Lời nhắc nhở (reminder_time)
        tk.Label(self, text="Thời gian nhắc nhở (YYYY-MM-DD HH:MM):").pack(anchor="w", padx=10)
        self.entry_reminder = tk.Entry(self, width=50)
        self.entry_reminder.pack(padx=10, pady=5)
        self.entry_reminder.insert(0, "") # Để trống nếu không đặt nhắc nhở

        # Hình ảnh đính kèm (image_url / path)
        tk.Label(self, text="Hình ảnh đính kèm:").pack(anchor="w", padx=10)
        frame_img = tk.Frame(self)
        frame_img.pack(fill="x", padx=10, pady=5)
        
        self.entry_image = tk.Entry(frame_img, width=38)
        self.entry_image.pack(side="left", padx=(0,5))
        btn_browse = tk.Button(frame_img, text="Chọn ảnh", command=self.browse_image)
        btn_browse.pack(side="left")

        # Nội dung
        tk.Label(self, text="Nội dung:").pack(anchor="w", padx=10)
        self.txt_content = tk.Text(self, height=6, width=50)
        self.txt_content.pack(padx=10, pady=5)

        # Nút Lưu
        btn_save = tk.Button(self, text="Lưu Ghi Chú", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.save_note)
        btn_save.pack(pady=15)

    def browse_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.jpeg")])
        if file_path:
            self.entry_image.delete(0, tk.END)
            self.entry_image.insert(0, file_path)

    def save_note(self):
        title = self.entry_title.get().strip()
        content = self.txt_content.get("1.0", tk.END).strip()
        category = self.cb_category.get()
        priority = self.cb_priority.get()
        
        # Lấy giá trị reminder_time và image_url (chuyển sang None nếu rỗng)
        reminder_time = self.entry_reminder.get().strip() or None
        image_url = self.entry_image.get().strip() or None

        if not title or not content:
            messagebox.showwarning("Cảnh báo", "Vui lòng điền đầy đủ Tiêu đề và Nội dung!")
            return

        # Gọi API Service với đầy đủ thông số
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