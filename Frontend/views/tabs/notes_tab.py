import tkinter as tk
from tkinter import ttk, messagebox
from Frontend.views.add_note_view import AddNoteWindow

class NotesTab(ttk.Frame):
    def __init__(self, parent, main_window, note_controller):
        super().__init__(parent)
        self.main_window = main_window 
        self.note_controller = note_controller
        self.note_map = {}
        self.selected_note_id = None
        self.current_search_keyword = ""
        self.edit_window_open = False

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
        self.detail_frame.configure(width=250)

        self.lbl_title = tk.Label(self.detail_frame, text="Tiêu đề: ", anchor="w", justify="left", font=("Arial", 10, "bold"), wraplength=230)
        self.lbl_category = tk.Label(self.detail_frame, text="Chủ đề: ", anchor="w", justify="left", font=("Arial", 10))
        self.lbl_priority = tk.Label(self.detail_frame, text="Mức độ: ", anchor="w", justify="left", font=("Arial", 10))
        self.lbl_status = tk.Label(self.detail_frame, text="Trạng thái: ", anchor="w", justify="left", font=("Arial", 10, "bold"))
        self.lbl_date = tk.Label(self.detail_frame, text="Ngày tạo: ", anchor="w", justify="left", font=("Arial", 10))
        self.lbl_reminder = tk.Label(self.detail_frame, text="Nhắc nhở: ", anchor="w", justify="left", font=("Arial", 10), fg="#E65100")
        self.lbl_preview = tk.Label(self.detail_frame, text="Nội dung:", anchor="nw", justify="left", wraplength=230, font=("Arial", 10), fg="#333333")
        self.lbl_info = tk.Label(self.detail_frame, text="Chọn ghi chú để xem chi tiết.", fg="#777777", wraplength=230, justify="left", font=("Arial", 9))

        for lbl in (self.lbl_title, self.lbl_category, self.lbl_priority, self.lbl_status, self.lbl_date, self.lbl_reminder, self.lbl_preview, self.lbl_info):
            lbl.pack(fill="x", pady=(0, 4))

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
            return

        self.lbl_title.config(text=f"Tiêu đề: {note.title}")
        self.lbl_category.config(text=f"Chủ đề: {note.category}")
        self.lbl_priority.config(text=f"Mức độ: {note.priority}")
        self.lbl_date.config(text=f"Ngày tạo: {note.create_at}")
        
        # Đổi màu trạng thái cho sinh động
        status_color = "#4CAF50" if note.status == "Đã hoàn thành" else "#E53935" if note.status == "Quá hạn" else "#F57C00"
        self.lbl_status.config(text=f"Trạng thái: {note.status}", fg=status_color)
        
        reminder_txt = note.reminder_time if note.reminder_time else "Không có"
        self.lbl_reminder.config(text=f"Nhắc nhở: {reminder_txt}")
        
        content = note.content if note.content else ""
        self.lbl_preview.config(text=f"Nội dung: {content[:150] + '...' if len(content) > 150 else content}")
        
        img_info = " (Có đính kèm ảnh)" if note.image_url else ""
        self.lbl_info.config(text=f"Nhấn nút Sửa hoặc nháy đúp để chỉnh sửa.{img_info}")

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