import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from PIL import Image, ImageTk
from Frontend.views.add_note_view import AddNoteWindow
from Frontend.utils import image_cache

class NotesTab(ttk.Frame):
    def __init__(self, parent, main_window, note_controller):
        super().__init__(parent)
        self.main_window = main_window 
        self.note_controller = note_controller
        self.note_map = {}
        self._all_notes = []  # Lưu toàn bộ dữ liệu để lọc Client-side
        self.selected_note_id = None
        self.current_search_keyword = ""
        self.edit_window_open = False
        self.current_pil_image = None
        self.tk_thumb_img = None

        # Filter state variables
        self.show_advanced_filter = tk.BooleanVar(value=False)
        self.filter_date_active = tk.BooleanVar(value=False)
        self.filter_cat_var = tk.StringVar(value="-- Tất cả --")
        self.filter_prio_var = tk.StringVar(value="-- Tất cả --")
        self.filter_status_var = tk.StringVar(value="-- Tất cả --")

        # Sorting state variables
        self._sort_col = None
        self._sort_reverse = False
        self._col_titles = {
            "title": "Tiêu đề",
            "category": "Chủ đề",
            "priority": "Mức độ",
            "status": "Trạng thái",
            "create_at": "Ngày tạo"
        }

        self._build_search_frame()
        self._build_filter_bar()
        self._build_filter_tags_frame()
        self._build_content_frame()
        self._build_action_buttons()

    def _build_search_frame(self):
        self.search_frame = tk.Frame(self, bg="#F5F7FB")
        self.search_frame.pack(fill="x", padx=10, pady=(6, 4))

        tk.Label(self.search_frame, text="🔎 Tìm kiếm:", bg="#F5F7FB", font=("Arial", 10, "bold")).pack(side="left")
        
        self.search_var = tk.StringVar()
        self.entry_search = tk.Entry(self.search_frame, textvariable=self.search_var, font=("Arial", 10), width=32)
        self.entry_search.pack(side="left", padx=(6, 8), ipady=3)
        self.entry_search.bind("<Return>", self.perform_search)
        self.entry_search.bind("<KeyRelease>", lambda e: self._on_search_key_release())

        tk.Button(
            self.search_frame, text="Tìm", bg="#1976D2", fg="white", font=("Arial", 9, "bold"),
            relief="flat", padx=12, pady=2, cursor="hand2", command=self.perform_search
        ).pack(side="left", padx=(0, 15))

        # Checkbox bật / tắt Lọc nâng cao
        self.chk_adv_filter = tk.Checkbutton(
            self.search_frame, text="Lọc nâng cao", variable=self.show_advanced_filter,
            bg="#F5F7FB", activebackground="#F5F7FB", font=("Arial", 10, "bold"),
            fg="#0288D1", selectcolor="#FFFFFF", cursor="hand2", command=self._toggle_advanced_filter
        )
        self.chk_adv_filter.pack(side="left")

    def _build_filter_bar(self):
        """Thanh bộ lọc nâng cao (Advanced Filter) gồm 4 tiêu chí + nút reset."""
        self.filter_container = tk.Frame(self, bg="#FFFFFF", bd=1, relief="solid")
        # Mặc định ẩn, chỉ hiện khi tích "⚡ Lọc nâng cao"

        filter_bar = tk.Frame(self.filter_container, bg="#FFFFFF", padx=10, pady=8)
        filter_bar.pack(fill="x")

        # 1. Bộ lọc Ngày tạo
        frame_date = tk.Frame(filter_bar, bg="#FFFFFF")
        frame_date.pack(side="left", padx=(0, 12))

        self.cb_date = tk.Checkbutton(
            frame_date, text="📅 Ngày:", variable=self.filter_date_active,
            bg="#FFFFFF", activebackground="#FFFFFF", font=("Arial", 9, "bold"),
            selectcolor="#FFFFFF", cursor="hand2", command=self._on_filter_changed
        )
        self.cb_date.pack(side="left", padx=(0, 2))

        self.cal_filter_date = DateEntry(
            frame_date, width=10, background='#1976D2', foreground='white',
            borderwidth=1, date_pattern='yyyy-mm-dd', font=("Arial", 9)
        )
        self.cal_filter_date.pack(side="left")
        self.cal_filter_date.bind("<<DateEntrySelected>>", lambda e: self._on_date_selected())

        # 2. Bộ lọc Chủ đề
        frame_cat = tk.Frame(filter_bar, bg="#FFFFFF")
        frame_cat.pack(side="left", padx=(0, 12))
        tk.Label(frame_cat, text="📂 Chủ đề:", bg="#FFFFFF", font=("Arial", 9, "bold")).pack(side="left", padx=(0, 4))
        
        self.cbo_cat = ttk.Combobox(
            frame_cat, textvariable=self.filter_cat_var, state="readonly", width=12, font=("Arial", 9)
        )
        self.cbo_cat["values"] = ["-- Tất cả --", "Chung", "Công việc", "Học tập", "Cá nhân"]
        self.cbo_cat.pack(side="left")
        self.cbo_cat.bind("<<ComboboxSelected>>", lambda e: self._on_filter_changed())

        # 3. Bộ lọc Mức độ: Thấp, Bình Thường, Cao
        frame_prio = tk.Frame(filter_bar, bg="#FFFFFF")
        frame_prio.pack(side="left", padx=(0, 12))
        tk.Label(frame_prio, text="⚡ Mức độ:", bg="#FFFFFF", font=("Arial", 9, "bold")).pack(side="left", padx=(0, 4))
        
        self.cbo_prio = ttk.Combobox(
            frame_prio, textvariable=self.filter_prio_var, state="readonly", width=12, font=("Arial", 9)
        )
        self.cbo_prio["values"] = ["-- Tất cả --", "Thấp", "Bình Thường", "Cao"]
        self.cbo_prio.pack(side="left")
        self.cbo_prio.bind("<<ComboboxSelected>>", lambda e: self._on_filter_changed())

        # 4. Bộ lọc Trạng thái
        frame_status = tk.Frame(filter_bar, bg="#FFFFFF")
        frame_status.pack(side="left", padx=(0, 12))
        tk.Label(frame_status, text="🔖 Trạng thái:", bg="#FFFFFF", font=("Arial", 9, "bold")).pack(side="left", padx=(0, 4))
        
        self.cbo_status = ttk.Combobox(
            frame_status, textvariable=self.filter_status_var, state="readonly", width=13, font=("Arial", 9)
        )
        self.cbo_status["values"] = ["-- Tất cả --", "Đang chờ", "Đã hoàn thành", "Quá hạn"]
        self.cbo_status.pack(side="left")
        self.cbo_status.bind("<<ComboboxSelected>>", lambda e: self._on_filter_changed())

        # 5. Nút Xóa bộ lọc (Màu đỏ rõ ràng, chữ đậm)
        btn_clear = tk.Button(
            filter_bar, text="✕ Xóa bộ lọc", bg="#DC2626", fg="white", font=("Arial", 9, "bold"),
            relief="flat", padx=10, pady=3, cursor="hand2", command=self.clear_filters
        )
        btn_clear.pack(side="right")

    def _build_filter_tags_frame(self):
        """Hàng hiển thị các tag bộ lọc đang active và số lượng kết quả."""
        self.frame_tags_row = tk.Frame(self, bg="#F5F7FB")
        # Mặc định ẩn cùng filter_container

        self.frame_tags_container = tk.Frame(self.frame_tags_row, bg="#F5F7FB")
        self.frame_tags_container.pack(side="left", fill="x")

        self.lbl_count_info = tk.Label(
            self.frame_tags_row, text="", bg="#F5F7FB", fg="#475569", font=("Arial", 9, "italic")
        )
        self.lbl_count_info.pack(side="right")

    def _toggle_advanced_filter(self):
        """Hiển thị hoặc ẩn thanh lọc nâng cao theo checkbox."""
        if self.show_advanced_filter.get():
            self.filter_container.pack(fill="x", padx=10, pady=(2, 4), after=self.search_frame)
            self.frame_tags_row.pack(fill="x", padx=10, pady=(0, 4), after=self.filter_container)
        else:
            self.filter_container.pack_forget()
            self.frame_tags_row.pack_forget()
            # Khi bỏ tích, reset các tiêu chí nâng cao về mặc định
            self.filter_date_active.set(False)
            self.filter_cat_var.set("-- Tất cả --")
            self.filter_prio_var.set("-- Tất cả --")
            self.filter_status_var.set("-- Tất cả --")
        
        self._apply_filters()

    def _on_date_selected(self):
        """Tự động kích hoạt checkbox ngày khi người dùng chọn ngày trên lịch."""
        self.filter_date_active.set(True)
        self._on_filter_changed()

    def _on_search_key_release(self):
        """Tự động tìm kiếm & lọc realtime khi người dùng nhập từ khóa."""
        self._apply_filters()

    def _on_filter_changed(self):
        """Kích hoạt áp dụng bộ lọc khi có bất kỳ tiêu chí nào thay đổi."""
        self._apply_filters()

    def clear_filters(self):
        """Reset toàn bộ các bộ lọc nâng cao về mặc định."""
        self.filter_date_active.set(False)
        self.filter_cat_var.set("-- Tất cả --")
        self.filter_prio_var.set("-- Tất cả --")
        self.filter_status_var.set("-- Tất cả --")
        self._apply_filters()

    def _sort_by(self, col: str):
        """Sắp xếp danh sách theo cột, toggle chiều A-Z / Z-A hoặc cũ-mới / mới-cũ."""
        if self._sort_col == col:
            self._sort_reverse = not self._sort_reverse
        else:
            self._sort_col = col
            self._sort_reverse = False

        self._update_heading_arrows()
        self._apply_filters()

    def _update_heading_arrows(self):
        """Cập nhật icon mũi tên ▲ (tăng dần) / ▼ (giảm dần) trên tiêu đề các cột."""
        for col, title in self._col_titles.items():
            if col == self._sort_col:
                arrow = " ▼" if self._sort_reverse else " ▲"
                self.tree.heading(col, text=f"{title}{arrow}")
            else:
                self.tree.heading(col, text=title)

    def _update_filter_tags(self, active_filters, count_shown, total_count):
        """Cập nhật các pill-tags bộ lọc đang áp dụng."""
        for child in self.frame_tags_container.winfo_children():
            child.destroy()

        if not active_filters:
            sort_info = f" | Sắp xếp: {self._col_titles.get(self._sort_col, '')} ({'Giảm dần' if self._sort_reverse else 'Tăng dần'})" if self._sort_col else ""
            self.lbl_count_info.config(text=f"Tổng số: {total_count} ghi chú{sort_info}")
            return

        tk.Label(
            self.frame_tags_container, text="Đang lọc:", bg="#F5F7FB", fg="#334155", font=("Arial", 8, "bold")
        ).pack(side="left", padx=(0, 4))

        for ftype, label_text, clear_cmd in active_filters:
            tag_frame = tk.Frame(self.frame_tags_container, bg="#E0F2FE", bd=1, relief="solid")
            tag_frame.pack(side="left", padx=2)

            tk.Label(
                tag_frame, text=label_text, bg="#E0F2FE", fg="#0369A1", font=("Arial", 8, "bold"), padx=4
            ).pack(side="left")

            btn_del = tk.Button(
                tag_frame, text="×", bg="#E0F2FE", fg="#0369A1", font=("Arial", 8, "bold"),
                bd=0, cursor="hand2", padx=3, pady=0, command=clear_cmd
            )
            btn_del.pack(side="left")

        sort_info = f" | Sắp xếp: {self._col_titles.get(self._sort_col, '')}" if self._sort_col else ""
        self.lbl_count_info.config(text=f"Hiển thị {count_shown} / {total_count} ghi chú (đã lọc){sort_info}")

    def _apply_filters(self):
        """Lọc danh sách ghi chú Client-side dựa trên từ khóa, bộ lọc nâng cao và sắp xếp hiện tại."""
        notes = list(self._all_notes)
        active_filters = []

        # 1. Tìm kiếm theo từ khóa (trong Tiêu đề, Nội dung, Chủ đề, Mức độ)
        keyword = self.search_var.get().strip().lower()
        if keyword:
            notes = [
                n for n in notes
                if keyword in (getattr(n, "title", "") or "").lower()
                or keyword in (getattr(n, "content", "") or "").lower()
                or keyword in (getattr(n, "category", "") or "").lower()
                or keyword in (getattr(n, "priority", "") or "").lower()
                or keyword in (getattr(n, "status", "") or "").lower()
            ]

        # 2. Áp dụng Bộ lọc nâng cao (nếu đang bật)
        if self.show_advanced_filter.get():
            # 2.1 Tiêu chí ngày
            if self.filter_date_active.get():
                try:
                    selected_date = self.cal_filter_date.get_date().strftime("%Y-%m-%d")
                except Exception:
                    selected_date = str(self.cal_filter_date.get())
                
                notes = [n for n in notes if str(getattr(n, "create_at", ""))[:10] == selected_date]
                
                def _clear_date():
                    self.filter_date_active.set(False)
                    self._apply_filters()
                    
                active_filters.append(("date", f"📅 {selected_date}", _clear_date))

            # 2.2 Tiêu chí chủ đề
            cat_val = self.filter_cat_var.get().strip()
            if cat_val and cat_val != "-- Tất cả --":
                notes = [n for n in notes if (getattr(n, "category", "") or "").strip().lower() == cat_val.lower()]
                
                def _clear_cat():
                    self.filter_cat_var.set("-- Tất cả --")
                    self._apply_filters()
                    
                active_filters.append(("category", f"📂 {cat_val}", _clear_cat))

            # 2.3 Tiêu chí mức độ (Thấp, Bình Thường, Cao)
            prio_val = self.filter_prio_var.get().strip()
            if prio_val and prio_val != "-- Tất cả --":
                notes = [n for n in notes if (getattr(n, "priority", "") or "").strip().lower() == prio_val.lower()]
                
                def _clear_prio():
                    self.filter_prio_var.set("-- Tất cả --")
                    self._apply_filters()
                    
                active_filters.append(("priority", f"⚡ {prio_val}", _clear_prio))

            # 2.4 Tiêu chí trạng thái
            status_val = self.filter_status_var.get().strip()
            if status_val and status_val != "-- Tất cả --":
                notes = [n for n in notes if (getattr(n, "status", "") or "").strip().lower() == status_val.lower()]
                
                def _clear_status():
                    self.filter_status_var.set("-- Tất cả --")
                    self._apply_filters()
                    
                active_filters.append(("status", f"🔖 {status_val}", _clear_status))

        # 3. Áp dụng sắp xếp trên kết quả lọc
        if self._sort_col:
            col = self._sort_col
            reverse = self._sort_reverse
            if col == "create_at":
                notes.sort(key=lambda n: str(getattr(n, "create_at", "") or ""), reverse=reverse)
            elif col == "priority":
                prio_weights = {"thấp": 1, "thap": 1, "bình thường": 2, "binh thuong": 2, "cao": 3}
                notes.sort(key=lambda n: prio_weights.get((getattr(n, "priority", "") or "").lower(), 0), reverse=reverse)
            else:
                notes.sort(key=lambda n: str(getattr(n, col, "") or "").lower(), reverse=reverse)

        self.render_notes(notes)
        self._update_filter_tags(active_filters, len(notes), len(self._all_notes))

    def _populate_category_combobox(self):
        """Cập nhật động các chủ đề xuất hiện trong danh sách ghi chú."""
        categories = set(["Chung", "Công việc", "Học tập", "Cá nhân"])
        for note in self._all_notes:
            cat = getattr(note, "category", None)
            if cat and cat.strip():
                categories.add(cat.strip())
        
        current = self.filter_cat_var.get()
        values = ["-- Tất cả --"] + sorted(list(categories))
        self.cbo_cat["values"] = values
        if current not in values:
            self.filter_cat_var.set("-- Tất cả --")

    def _build_content_frame(self):
        content_frame = tk.Frame(self, bg="#F5F7FB")
        content_frame.pack(fill="both", expand=True, padx=5, pady=5)

        # Treeview (Bảng danh sách)
        frame_list = tk.Frame(content_frame, bg="#F5F7FB")
        frame_list.pack(side="left", fill="both", expand=True)

        columns = ("title", "category", "priority", "status", "create_at")
        self.tree = ttk.Treeview(frame_list, columns=columns, show="headings", height=10)
        
        for col, text, width in [("title", "Tiêu đề", 220), ("category", "Chủ đề", 90), 
                                 ("priority", "Mức độ", 90), ("status", "Trạng thái", 110), 
                                 ("create_at", "Ngày tạo", 100)]:
            # Click vào heading để sắp xếp
            self.tree.heading(col, text=text, command=lambda c=col: self._sort_by(c))
            self.tree.column(col, width=width, anchor="w" if col == "title" else "center")

        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        # Bắt sự kiện double-click có kiểm tra vùng click (tránh click vào heading bị mở popup)
        self.tree.bind("<Double-1>", self._on_tree_double_click)

        scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Khung chi tiết
        self.detail_frame = ttk.LabelFrame(content_frame, text="Thông tin ghi chú", padding=(10, 10))
        self.detail_frame.pack(side="right", fill="y", padx=(10, 0), pady=0)
        self.detail_frame.configure(width=290)

        self.lbl_title = tk.Label(self.detail_frame, text="Tiêu đề: ", anchor="w", justify="left", font=("Arial", 10, "bold"), wraplength=270)
        self.lbl_category = tk.Label(self.detail_frame, text="Chủ đề: ", anchor="w", justify="left", font=("Arial", 10))
        self.lbl_priority = tk.Label(self.detail_frame, text="Mức độ: ", anchor="w", justify="left", font=("Arial", 10))
        self.lbl_status = tk.Label(self.detail_frame, text="Trạng thái: ", anchor="w", justify="left", font=("Arial", 10, "bold"))
        self.lbl_date = tk.Label(self.detail_frame, text="Ngày tạo: ", anchor="w", justify="left", font=("Arial", 10))
        self.lbl_reminder = tk.Label(self.detail_frame, text="Nhắc nhở: ", anchor="w", justify="left", font=("Arial", 10), fg="#E65100")
        self.lbl_preview = tk.Label(self.detail_frame, text="Nội dung:", anchor="nw", justify="left", wraplength=270, font=("Arial", 10), fg="#333333")

        # Ô hiển thị ảnh đính kèm (dưới nội dung, to 1 chút)
        self.frame_image_preview = tk.LabelFrame(self.detail_frame, text="🖼️ Ảnh đính kèm (Nhấn để phóng to)", font=("Arial", 9, "bold"))
        self.lbl_img_preview = tk.Label(self.frame_image_preview, text="", cursor="hand2")
        self.lbl_img_preview.pack(padx=5, pady=5)
        self.lbl_img_preview.bind("<Button-1>", lambda e: self._open_fullscreen_image())

        self.lbl_info = tk.Label(self.detail_frame, text="Chọn ghi chú để xem chi tiết.", fg="#777777", wraplength=270, justify="left", font=("Arial", 9))

        for lbl in (self.lbl_title, self.lbl_category, self.lbl_priority, self.lbl_status, self.lbl_date, self.lbl_reminder, self.lbl_preview):
            lbl.pack(fill="x", pady=(0, 4))
        
        # Ô ảnh đính kèm - pack sau lbl_preview, ẩn mặc định
        self.frame_image_preview.pack(fill="x", pady=(0, 4))
        self.frame_image_preview.pack_forget()  # Ẩn ban đầu
        
        self.lbl_info.pack(fill="x", pady=(4, 0))

    def _on_tree_double_click(self, event):
        """Chỉ mở sửa khi double-click vào row/cell thực sự, bỏ qua nếu click vào heading/separator."""
        region = self.tree.identify_region(event.x, event.y)
        if region in ("heading", "separator"):
            return
        item = self.tree.identify_row(event.y)
        if not item:
            return
        self.open_selected_note()

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
        if success and isinstance(data, list):
            self._all_notes = data
            self._populate_category_combobox()
            self._apply_filters()
        else:
            self._all_notes = []
            self.render_notes([])
            if not success:
                messagebox.showerror("Lỗi", str(data))

    def perform_search(self, event=None):
        """Thực hiện tìm kiếm kết hợp với bộ lọc."""
        self._apply_filters()

    def render_notes(self, notes):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.note_map.clear()
        self.selected_note_id = None
        self.update_detail_panel(None)

        if notes:
            for index, note in enumerate(notes):
                self.note_map[str(note.id)] = note
                
                # Highlight màu dòng theo trạng thái (chữ đen/đậm rõ ràng trên nền pastel nhẹ)
                status_str = (getattr(note, "status", "") or "").strip()
                if status_str == "Quá hạn":
                    tag = "overdue"
                elif status_str == "Đã hoàn thành":
                    tag = "done"
                else:
                    tag = "evenrow" if index % 2 == 0 else "oddrow"

                self.tree.insert("", "end", iid=str(note.id), 
                                 values=(note.title, note.category, note.priority, note.status, note.create_at), 
                                 tags=(tag,))
            
            # Cấu hình màu dòng rõ nét, tương phản cao, dễ đọc
            self.tree.tag_configure("evenrow", background="#FFFFFF", foreground="#1E293B")
            self.tree.tag_configure("oddrow", background="#F8FAFC", foreground="#1E293B")
            self.tree.tag_configure("overdue", background="#FEE2E2", foreground="#991B1B")
            self.tree.tag_configure("done", background="#DCFCE7", foreground="#166534")

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
        
        status_color = "#16A34A" if note.status == "Đã hoàn thành" else "#DC2626" if note.status == "Quá hạn" else "#D97706"
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

    def reload_from_db(self):
        """Tự động tải lại danh sách mới nhất từ database và áp dụng bộ lọc/sắp xếp hiện tại."""
        success, data = self.note_controller.get_notes()
        if success and isinstance(data, list):
            self._all_notes = data
            self._populate_category_combobox()
            self._apply_filters()
        else:
            self._all_notes = []
            self.render_notes([])
            if not success:
                messagebox.showerror("Lỗi", str(data))

    def load_data(self):
        """Nạp dữ liệu (hoặc khi bấm nút Tải lại): reset ô tìm kiếm và nạp lại từ DB."""
        self.search_var.set("")
        self.current_search_keyword = ""
        self.reload_from_db()

    def perform_search(self, event=None):
        """Thực hiện tìm kiếm kết hợp với bộ lọc."""
        self._apply_filters()

    def open_add_note(self):
        """Mở cửa sổ thêm ghi chú mới và tự động tải lại ngay khi hoàn tất."""
        window = AddNoteWindow(self.main_window, on_success_callback=self.reload_from_db)
        self.main_window.wait_window(window)
        self.reload_from_db()
        if hasattr(self.main_window, "stats_tab"):
            self.main_window.stats_tab.load_statistics() 

    def open_selected_note(self):
        """Mở cửa sổ sửa ghi chú và tự động tải lại ngay khi cập nhật thành công."""
        if self.edit_window_open or not self.selected_note_id:
            if not self.selected_note_id:
                messagebox.showwarning("Chú ý", "Vui lòng chọn ghi chú trước khi sửa.")
            return

        note = self.note_map.get(self.selected_note_id)
        self.edit_window_open = True
        window = AddNoteWindow(self.main_window, note_data=note, on_success_callback=self.reload_from_db)
        self.main_window.wait_window(window)
        self.edit_window_open = False
        self.reload_from_db()
        if hasattr(self.main_window, "stats_tab"):
            self.main_window.stats_tab.load_statistics()

    def delete_selected_note(self):
        """Xóa ghi chú đã chọn và tự động tải lại danh sách từ database."""
        if not self.selected_note_id:
            messagebox.showwarning("Chú ý", "Vui lòng chọn ghi chú cần xóa.")
            return

        note = self.note_map.get(self.selected_note_id)
        if messagebox.askyesno("Xác nhận", f"Bạn có chắc muốn xóa ghi chú: '{note.title}'?"):
            success, msg = self.note_controller.delete_note(self.selected_note_id)
            if success:
                messagebox.showinfo("Thành công", msg)
                self.reload_from_db()
                if hasattr(self.main_window, "stats_tab"):
                    self.main_window.stats_tab.load_statistics()
            else:
                messagebox.showerror("Lỗi", msg)
