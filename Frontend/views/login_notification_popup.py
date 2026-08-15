import tkinter as tk
from tkinter import ttk


class LoginNotificationPopup(tk.Toplevel):
    def __init__(self, parent, notifications, on_view_all_callback=None):
        super().__init__(parent)
        self.title("Thông báo lịch hẹn")
        self.geometry("420x360")
        self.configure(bg="#FFFFFF")
        self.resizable(False, False)

        self.parent = parent
        self.notifications = notifications or []
        self.on_view_all_callback = on_view_all_callback

        self.transient(parent)
        self.grab_set()  # Modal popup
        self._center_window()

        self._build_ui()

    def _center_window(self):
        self.update_idletasks()
        p_x = self.parent.winfo_rootx()
        p_y = self.parent.winfo_rooty()
        p_w = self.parent.winfo_width()
        p_h = self.parent.winfo_height()

        w = 420
        h = 360
        x = p_x + (p_w - w) // 2
        y = p_y + (p_h - h) // 2
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _build_ui(self):
        # Header banner
        header = tk.Frame(self, bg="#EFF6FF", height=70)
        header.pack(fill="x", side="top")

        lbl_icon = tk.Label(header, text="⏰", font=("Arial", 22), bg="#EFF6FF")
        lbl_icon.pack(side="left", padx=(20, 10), pady=15)

        title_frame = tk.Frame(header, bg="#EFF6FF")
        title_frame.pack(side="left", fill="both", expand=True, pady=12)

        count = len(self.notifications)
        lbl_title = tk.Label(
            title_frame,
            text=f"Bạn có {count} thông báo mới!",
            font=("Arial", 12, "bold"),
            fg="#1E40AF",
            bg="#EFF6FF",
            anchor="w"
        )
        lbl_title.pack(fill="x")

        lbl_sub = tk.Label(
            title_frame,
            text="Các lịch hẹn và ghi chú cần chú ý:",
            font=("Arial", 9),
            fg="#64748B",
            bg="#EFF6FF",
            anchor="w"
        )
        lbl_sub.pack(fill="x", pady=(2, 0))

        # Danh sách thông báo
        list_frame = tk.Frame(self, bg="#FFFFFF")
        list_frame.pack(fill="both", expand=True, padx=20, pady=15)

        canvas = tk.Canvas(list_frame, bg="#FFFFFF", highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scroll_content = tk.Frame(canvas, bg="#FFFFFF")

        scroll_content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas_window = canvas.create_window((0, 0), window=scroll_content, anchor="nw")
        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfig(canvas_window, width=e.width)
        )
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        if len(self.notifications) > 3:
            scrollbar.pack(side="right", fill="y")

        for notif in self.notifications[:10]:
            item_card = tk.Frame(scroll_content, bg="#F8FAFC", highlightbackground="#E2E8F0", highlightthickness=1)
            item_card.pack(fill="x", pady=3, padx=2)

            dot = tk.Label(item_card, text="●", font=("Arial", 9), fg="#2563EB", bg="#F8FAFC")
            dot.pack(side="left", padx=(8, 4), pady=6, anchor="n")

            content = tk.Frame(item_card, bg="#F8FAFC")
            content.pack(side="left", fill="both", expand=True, pady=6, padx=(0, 8))

            t_lbl = tk.Label(
                content,
                text=notif.title if hasattr(notif, "title") else notif.get("title", ""),
                font=("Arial", 9, "bold"),
                fg="#1E293B",
                bg="#F8FAFC",
                anchor="w"
            )
            t_lbl.pack(fill="x")

            m_txt = notif.message if hasattr(notif, "message") else notif.get("message", "")
            m_lbl = tk.Label(
                content,
                text=m_txt,
                font=("Arial", 8),
                fg="#64748B",
                bg="#F8FAFC",
                anchor="w",
                wraplength=290,
                justify="left"
            )
            m_lbl.pack(fill="x", pady=(2, 0))

        # Footer Buttons
        footer = tk.Frame(self, bg="#FFFFFF", height=50)
        footer.pack(fill="x", side="bottom", padx=20, pady=(0, 15))

        btn_dismiss = tk.Button(
            footer,
            text="Đã hiểu",
            font=("Arial", 10),
            bg="#F1F5F9",
            fg="#475569",
            activebackground="#E2E8F0",
            bd=0,
            cursor="hand2",
            padx=16,
            pady=6,
            command=self.destroy
        )
        btn_dismiss.pack(side="left")

        btn_view_all = tk.Button(
            footer,
            text="Xem tất cả ➔",
            font=("Arial", 10, "bold"),
            bg="#2563EB",
            fg="#FFFFFF",
            activebackground="#1D4ED8",
            bd=0,
            cursor="hand2",
            padx=16,
            pady=6,
            command=self._on_view_all
        )
        btn_view_all.pack(side="right")

    def _on_view_all(self):
        self.destroy()
        if self.on_view_all_callback:
            self.on_view_all_callback()
