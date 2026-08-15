import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from Frontend.controllers.notification_controller import NotificationController


class NotificationPanel(tk.Toplevel):
    def __init__(self, parent, on_update_callback=None):
        super().__init__(parent)
        self.title("Thông báo")
        self.geometry("450x520")
        self.configure(bg="#F5F7FB")
        self.resizable(False, False)

        self.parent = parent
        self.on_update_callback = on_update_callback
        self.controller = NotificationController()
        self.notifications = []

        # Hiển thị modal nổi trên cửa sổ cha
        self.transient(parent)
        self._center_window()

        self._build_header()
        self._build_list_area()
        self._build_footer()

        self.load_notifications()

    def _center_window(self):
        self.update_idletasks()
        p_x = self.parent.winfo_rootx()
        p_y = self.parent.winfo_rooty()
        p_w = self.parent.winfo_width()
        p_h = self.parent.winfo_height()

        w = 450
        h = 520
        # Căn sang góc phải trên của cửa sổ cha
        x = p_x + p_w - w - 20
        y = p_y + 60
        if x < 0:
            x = p_x + (p_w - w) // 2
        if y < 0:
            y = p_y + (p_h - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_header(self):
        header = tk.Frame(self, bg="#FFFFFF", height=50)
        header.pack(fill="x", side="top")

        # Tiêu đề
        lbl_title = tk.Label(
            header,
            text="🔔 Thông báo",
            font=("Arial", 13, "bold"),
            bg="#FFFFFF",
            fg="#1E293B"
        )
        lbl_title.pack(side="left", padx=15, pady=12)

        # Nút Đã đọc hết
        btn_mark_all = tk.Button(
            header,
            text="✓ Đã đọc hết",
            font=("Arial", 9, "bold"),
            bg="#E0F2FE",
            fg="#0369A1",
            activebackground="#BAE6FD",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=4,
            command=self.handle_mark_all_read
        )
        btn_mark_all.pack(side="right", padx=15, pady=10)

        # Đường kẻ phân cách
        sep = tk.Frame(self, bg="#E2E8F0", height=1)
        sep.pack(fill="x", side="top")

    def _build_list_area(self):
        container = tk.Frame(self, bg="#F5F7FB")
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(container, bg="#F5F7FB", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas, bg="#F5F7FB")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.bind(
            "<Configure>",
            lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width)
        )

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bắt sự kiện cuộn chuột
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _on_mousewheel(self, event):
        if self.winfo_exists():
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _build_footer(self):
        sep = tk.Frame(self, bg="#E2E8F0", height=1)
        sep.pack(fill="x", side="bottom")

        footer = tk.Frame(self, bg="#FFFFFF", height=45)
        footer.pack(fill="x", side="bottom")

        btn_clear_all = tk.Button(
            footer,
            text="🗑 Xóa tất cả",
            font=("Arial", 9),
            bg="#FEE2E2",
            fg="#DC2626",
            activebackground="#FCA5A5",
            bd=0,
            cursor="hand2",
            padx=10,
            pady=4,
            command=self.handle_clear_all
        )
        btn_clear_all.pack(side="left", padx=15, pady=8)

        btn_close = tk.Button(
            footer,
            text="Đóng",
            font=("Arial", 9),
            bg="#E2E8F0",
            fg="#475569",
            activebackground="#CBD5E1",
            bd=0,
            cursor="hand2",
            padx=12,
            pady=4,
            command=self.destroy
        )
        btn_close.pack(side="right", padx=15, pady=8)

    def load_notifications(self):
        # Xóa các widget cũ
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        success, data = self.controller.get_notifications()
        if not success or not data:
            self._show_empty_state()
            if self.on_update_callback:
                self.on_update_callback()
            return

        self.notifications = data
        for notif in self.notifications:
            self._render_notification_item(notif)

        if self.on_update_callback:
            self.on_update_callback()

    def _show_empty_state(self):
        empty_frame = tk.Frame(self.scrollable_frame, bg="#F5F7FB")
        empty_frame.pack(fill="both", expand=True, pady=60)

        tk.Label(
            empty_frame,
            text="🎉",
            font=("Arial", 32),
            bg="#F5F7FB"
        ).pack(pady=(0, 10))

        tk.Label(
            empty_frame,
            text="Bạn không có thông báo nào",
            font=("Arial", 11, "bold"),
            fg="#64748B",
            bg="#F5F7FB"
        ).pack()

        tk.Label(
            empty_frame,
            text="Khi có lịch hẹn hoặc nhắc nhở, thông báo sẽ xuất hiện tại đây.",
            font=("Arial", 9),
            fg="#94A3B8",
            bg="#F5F7FB"
        ).pack(pady=4)

    def _render_notification_item(self, notif):
        is_unread = not notif.is_read

        # Kiểu dáng: Chưa đọc (Đậm, nền nổi), Đã đọc (Nhạt, nền mờ)
        bg_color = "#EFF6FF" if is_unread else "#FFFFFF"
        border_color = "#BFDBFE" if is_unread else "#E2E8F0"
        title_font = ("Arial", 10, "bold") if is_unread else ("Arial", 10, "normal")
        title_color = "#1E3A8A" if is_unread else "#64748B"
        msg_font = ("Arial", 9, "bold") if is_unread else ("Arial", 9, "normal")
        msg_color = "#1F2937" if is_unread else "#94A3B8"
        dot_color = "#2563EB" if is_unread else "#CBD5E1"

        card = tk.Frame(
            self.scrollable_frame,
            bg=bg_color,
            highlightbackground=border_color,
            highlightthickness=1,
            bd=0,
            cursor="hand2"
        )
        card.pack(fill="x", expand=True, pady=4, padx=2)

        # Cột chỉ báo chấm tròn
        dot_label = tk.Label(
            card,
            text="●",
            font=("Arial", 10),
            fg=dot_color,
            bg=bg_color
        )
        dot_label.pack(side="left", padx=(10, 6), pady=8, anchor="n")

        # Khung nội dung
        content_frame = tk.Frame(card, bg=bg_color)
        content_frame.pack(side="left", fill="both", expand=True, pady=6)

        # Tiêu đề thông báo
        lbl_title = tk.Label(
            content_frame,
            text=notif.title,
            font=title_font,
            fg=title_color,
            bg=bg_color,
            anchor="w",
            justify="left"
        )
        lbl_title.pack(fill="x", anchor="w")

        # Nội dung chi tiết
        lbl_msg = tk.Label(
            content_frame,
            text=notif.message,
            font=msg_font,
            fg=msg_color,
            bg=bg_color,
            anchor="w",
            justify="left",
            wraplength=310
        )
        lbl_msg.pack(fill="x", anchor="w", pady=(2, 2))

        # Thời gian
        time_text = self._format_time(notif.created_at)
        lbl_time = tk.Label(
            content_frame,
            text=time_text,
            font=("Arial", 8),
            fg="#94A3B8",
            bg=bg_color,
            anchor="w"
        )
        lbl_time.pack(fill="x", anchor="w")

        # Nút xóa từng mục
        btn_delete = tk.Button(
            card,
            text="✕",
            font=("Arial", 9, "bold"),
            fg="#94A3B8",
            bg=bg_color,
            activeforeground="#DC2626",
            activebackground=bg_color,
            bd=0,
            cursor="hand2",
            padx=8,
            command=lambda n_id=notif.id: self.handle_delete_one(n_id)
        )
        btn_delete.pack(side="right", padx=6, pady=6, anchor="n")

        # Click vào bất kỳ phần nào của card để đánh dấu đã đọc
        def on_card_click(event, n_id=notif.id, unread=is_unread):
            if unread:
                self.controller.mark_as_read(n_id)
                self.load_notifications()

        card.bind("<Button-1>", on_card_click)
        lbl_title.bind("<Button-1>", on_card_click)
        lbl_msg.bind("<Button-1>", on_card_click)
        lbl_time.bind("<Button-1>", on_card_click)
        dot_label.bind("<Button-1>", on_card_click)
        content_frame.bind("<Button-1>", on_card_click)

    def _format_time(self, iso_str: str) -> str:
        if not iso_str:
            return ""
        try:
            from datetime import timezone, timedelta
            raw_str = str(iso_str).replace("Z", "+00:00")
            dt = datetime.fromisoformat(raw_str)
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            # Chuyển đổi sang múi giờ Việt Nam (UTC+7)
            vn_tz = timezone(timedelta(hours=7))
            return dt.astimezone(vn_tz).strftime("%d/%m/%Y %H:%M")
        except Exception:
            return str(iso_str)[:16]

    def handle_mark_all_read(self):
        self.controller.mark_all_as_read()
        self.load_notifications()

    def handle_delete_one(self, notif_id: str):
        self.controller.delete_notification(notif_id)
        self.load_notifications()

    def handle_clear_all(self):
        if not self.notifications:
            return
        if messagebox.askyesno("Xác nhận", "Bạn có chắc chắn muốn xóa toàn bộ thông báo?"):
            self.controller.delete_all_notifications()
            self.load_notifications()
