import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from Frontend.views.add_note_view import AddNoteWindow
from Frontend.utils import image_cache

class NotesTab(ttk.Frame):
    def __init__(self, parent, main_window, note_controller):
        super().__init__(parent)
        self.main_window = main_window 
        self.note_controller = note_controller
        self.note_map = {}
        self.selected_note_id = None
        self.current_search_keyword = ""
        self.edit_window_open = False
        self.current_pil_image = None
        self.tk_thumb_img = None

        self._build_search_frame()
        self._build_content_frame()
        self._build_action_buttons()

    def _build_search_frame(self):
        search_frame = tk.Frame(self, bg="#F5F7FB")
        search_frame.pack(fill="x", padx=10, pady=(5, 5))

        tk.Label(search_frame, text="🔎 Tìm kiếm:", bg="#F5F7FB", font=("Arial", 10, "bold")).pack(side="left")
        
        self.search_var = tk.StringVar()
        self.entry_search = tk.Entry(search_frame, textvariable=self.search_var, font=("Arial", 10), width=35)
        self.entry_search.pack(side="left", padx=(5, 10), ipady=3)
        self.entry_search.bind("<Return>", self.perform_search)

        tk.Button(
            search_frame, text="Tìm", bg="#1976D2", fg="white", font=("Arial", 9, "bold"),
            relief="flat", padx=10, cursor="hand2", command=self.perform_search
        ).pack(side="left")

    def _build_content_frame(self):
        content_frame = tk.Frame(self, bg="#F5F7FB")
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Treeview (Bảng danh sách)
        frame_list = tk.Frame(content_frame, bg="#F5F7FB")
        frame_list.pack(side="left", fill="both", expand=True)

        columns = ("title", "category", "priority", "status", "create_at")
        self.tree = ttk.Treeview(frame_list, columns=columns, show="headings", height=10)
        
        for col, text, width in [("title", "Tiêu đề", 180), ("category", "Chủ đề", 80), 
                                 ("priority", "Mức độ", 80), ("status", "Trạng thái", 100), 
                                 ("create_at", "Ngày tạo", 90)]:
            self.tree.heading(col, text=text)
            self.tree.column(col, width=width, anchor="w" if col == "title" else "center")

        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", lambda e: self.open_selected_note())

        scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Khung chi tiết
        self.detail_frame = ttk.LabelFrame(content_frame, text="Thông tin ghi chú", padding=(10, 10))
        self.detail_frame.pack(side="right", fill="y", padx=(10, 0), pady=0)
        self.detail_frame.configure(width=280)

        self.lbl_title = tk.Label(self.detail_frame, text="Tiêu đề: ", anchor="w", justify="left", font=("Arial", 10, "bold"), wraplength=260)
        self.lbl_category = tk.Label(self.detail_frame, text="Chủ đề: ", anchor="w", justify="left", font=("Arial", 10))
        self.lbl_priority = tk.Label(self.detail_frame, text="Mức độ: ", anchor="w", justify="left", font=("Arial", 10))
        self.lbl_status = tk.Label(self.detail_frame, text="Trạng thái: ", anchor="w", justify="left", font=("Arial", 10, "bold"))
        self.lbl_date = tk.Label(self.detail_frame, text="Ngày tạo: ", anchor="w", justify="left", font=("Arial", 10))
        self.lbl_reminder = tk.Label(self.detail_frame, text="Nhắc nhở: ", anchor="w", justify="left", font=("Arial", 10), fg="#E65100")
        self.lbl_preview = tk.Label(self.detail_frame, text="Nội dung:", anchor="nw", justify="left", wraplength=260, font=("Arial", 10), fg="#333333")

        # Ô hiển thị ảnh đính kèm (dưới nội dung, to 1 chút)
        self.frame_image_preview = tk.LabelFrame(self.detail_frame, text="🖼️ Ảnh đính kèm (Nhấn để phóng to)", font=("Arial", 9, "bold"))
        self.lbl_img_preview = tk.Label(self.frame_image_preview, text="", cursor="hand2")
        self.lbl_img_preview.pack(padx=5, pady=5)
        self.lbl_img_preview.bind("<Button-1>", lambda e: self._open_fullscreen_image())

        self.lbl_info = tk.Label(self.detail_frame, text="Chọn ghi chú để xem chi tiết.", fg="#777777", wraplength=260, justify="left", font=("Arial", 9))

        for lbl in (self.lbl_title, self.lbl_category, self.lbl_priority, self.lbl_status, self.lbl_date, self.lbl_reminder, self.lbl_preview):
            lbl.pack(fill="x", pady=(0, 4))
        
        # Ô ảnh đính kèm - pack sau lbl_preview, ẩn mặc định
        self.frame_image_preview.pack(fill="x", pady=(0, 4))
        self.frame_image_preview.pack_forget()  # Ẩn ban đầu
        
        self.lbl_info.pack(fill="x", pady=(4, 0))

    def _build_action_buttons(self):
        frame_btn = tk.Frame(self, bg="#F5F7FB")
        frame_btn.pack(fill="x", padx=5, pady=10)

        buttons = [
            ("+ Thêm Ghi Chú", "#0288D1", self.open_add_note, "left"),
            ("✏️ Sửa", "#4CAF50", self.open_selected_note, "left"),
            ("🗑️ Xóa", "#E53935", self.delete_selected_note, "left"),
            ("🔄 Tải lại", "#E0E0E0", self.load_data, "right")
        ]

        for text, bg, cmd, side in buttons:
            fg = "white" if bg != "#E0E0E0" else "#333333"
            tk.Button(frame_btn, text=text, bg=bg, fg=fg, font=("Arial", 10, "bold"), 
                      relief="flat", padx=12, pady=6, cursor="hand2", command=cmd).pack(side=side, padx=(0 if side=="right" else 5))

    def load_data(self):
        self.search_var.set("")
        self.current_search_keyword = ""
        success, data = self.note_controller.get_notes()
        self.render_notes(data if success else [])
        if not success:
            messagebox.showerror("Lỗi", str(data))

    def perform_search(self, event=None):
        keyword = self.search_var.get().strip()
        self.current_search_keyword = keyword
        if not keyword:
            self.load_data()
            return
            
        success, data = self.note_controller.search_notes(keyword)
        self.render_notes(data if success else [])
        if not success:
            messagebox.showerror("Lỗi", str(data))

    def render_notes(self, notes):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.note_map.clear()
        self.selected_note_id = None
        self.update_detail_panel(None)

        if notes:
            for index, note in enumerate(notes):
                self.note_map[str(note.id)] = note
                tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.tree.insert("", "end", iid=str(note.id), 
                                 values=(note.title, note.category, note.priority, note.status, note.create_at), 
                                 tags=(tag,))
            
            self.tree.tag_configure("evenrow", background="#FFFFFF")
            self.tree.tag_configure("oddrow", background="#F3F7FF")

            # Pre-fetch ảnh của tất cả ghi chú vào cache RAM ngầm
            urls = [note.image_url for note in notes if getattr(note, "image_url", None)]
            image_cache.prefetch_many(urls)

    def on_tree_select(self, event=None):
        selection = self.tree.selection()
        if selection:
            self.selected_note_id = selection[0]
            self.update_detail_panel(self.note_map.get(self.selected_note_id))

    def update_detail_panel(self, note):
        if not note:
            self.lbl_title.config(text="Tiêu đề: ")
            self.lbl_category.config(text="Chủ đề: ")
            self.lbl_priority.config(text="Mức độ: ")
            self.lbl_status.config(text="Trạng thái: ", fg="black")
            self.lbl_date.config(text="Ngày tạo: ")
            self.lbl_reminder.config(text="Nhắc nhở: ")
            self.lbl_preview.config(text="Nội dung:")
            self.lbl_info.config(text="Chọn ghi chú để xem chi tiết.")
            self._hide_image_preview()
            return

        self.lbl_title.config(text=f"Tiêu đề: {note.title}")
        self.lbl_category.config(text=f"Chủ đề: {note.category}")
        self.lbl_priority.config(text=f"Mức độ: {note.priority}")
        self.lbl_date.config(text=f"Ngày tạo: {note.create_at}")
        
        status_color = "#4CAF50" if note.status == "Đã hoàn thành" else "#E53935" if note.status == "Quá hạn" else "#F57C00"
        self.lbl_status.config(text=f"Trạng thái: {note.status}", fg=status_color)
        
        reminder_txt = note.reminder_time if note.reminder_time else "Không có"
        self.lbl_reminder.config(text=f"Nhắc nhở: {reminder_txt}")
        
        content = note.content if note.content else ""
        self.lbl_preview.config(text=f"Nội dung: {content[:150] + '...' if len(content) > 150 else content}")
        
        img_info = " (Có đính kèm ảnh)" if note.image_url else ""
        self.lbl_info.config(text=f"Nhấn nút Sửa hoặc nháy đúp để chỉnh sửa.{img_info}")

        if note.image_url:
            self._load_and_display_image(note.image_url)
        else:
            self._hide_image_preview()

    def _hide_image_preview(self):
        self.current_pil_image = None
        self.tk_thumb_img = None
        self.frame_image_preview.pack_forget()

    def _load_and_display_image(self, image_url: str):
        self.frame_image_preview.pack(fill="x", pady=(0, 4))

        # Kiểm tra cache trước — hiển thị ngay nếu đã có
        cached = image_cache.get(image_url)
        if cached:
            self._show_image_thumbnail(cached)
            return

        # Chưa có trong cache — hiện trạng thái chờ và fetch ngầm
        self.current_pil_image = None
        self.lbl_img_preview.config(image="", text="⏳ Đang tải ảnh...", fg="#666666", font=("Arial", 9))

        def _on_fetched(url, img):
            if img:
                self.after(0, lambda: self._show_image_thumbnail(img))
            else:
                self.after(0, lambda: self.lbl_img_preview.config(
                    image="", text="❌ Không thể tải ảnh", fg="red"
                ))

        image_cache.prefetch(image_url, on_done=_on_fetched)

    def _show_image_thumbnail(self, raw_img: Image.Image):
        try:
            self.current_pil_image = raw_img
            thumb = raw_img.copy()
            thumb.thumbnail((240, 160), Image.Resampling.LANCZOS)
            self.tk_thumb_img = ImageTk.PhotoImage(thumb)
            self.lbl_img_preview.config(image=self.tk_thumb_img, text="")
        except Exception as e:
            self.lbl_img_preview.config(text=f"❌ Lỗi xử lý ảnh: {e}", fg="red")

    def _open_fullscreen_image(self):
        if not self.current_pil_image:
            return

        top = tk.Toplevel(self)
        top.title("Xem ảnh đầy đủ")
        top.geometry("800x650")

        try:
            full_img = self.current_pil_image.copy()
            full_img.thumbnail((780, 580), Image.Resampling.LANCZOS)
            tk_full = ImageTk.PhotoImage(full_img)

            lbl = tk.Label(top, image=tk_full, bg="#1E1E1E")
            lbl.image = tk_full # Giữ reference tránh garbage collector
            lbl.pack(fill="both", expand=True, padx=5, pady=5)

            btn_close = tk.Button(
                top, text="Đóng (Esc)", bg="#E53935", fg="white", font=("Arial", 10, "bold"),
                relief="flat", padx=15, pady=4, cursor="hand2", command=top.destroy
            )
            btn_close.pack(pady=(0, 8))

            top.bind("<Escape>", lambda e: top.destroy())
        except Exception as e:
            messagebox.showerror("Lỗi", f"Không thể phóng to ảnh: {e}")

    def open_add_note(self):
        AddNoteWindow(self.main_window)
        self.load_data()
        self.main_window.stats_tab.load_statistics() 

    def open_selected_note(self):
        if self.edit_window_open or not self.selected_note_id:
            if not self.selected_note_id:
                messagebox.showwarning("Chú ý", "Vui lòng chọn ghi chú trước khi sửa.")
            return

        note = self.note_map.get(self.selected_note_id)
        self.edit_window_open = True
        self.main_window.wait_window(AddNoteWindow(self.main_window, note_data=note))
        self.edit_window_open = False
        self.perform_search() if self.current_search_keyword else self.load_data()
        self.main_window.stats_tab.load_statistics()

    def delete_selected_note(self):
        if not self.selected_note_id:
            messagebox.showwarning("Chú ý", "Vui lòng chọn ghi chú cần xóa.")
            return

        note = self.note_map.get(self.selected_note_id)
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa ghi chú: '{note.title}'?"):
            success, msg = self.note_controller.delete_note(self.selected_note_id)
            if success:
                messagebox.showinfo("Thành công", msg)
                self.perform_search() if self.current_search_keyword else self.load_data()
                self.main_window.stats_tab.load_statistics()
            else:
                messagebox.showerror("Lỗi", msg)
