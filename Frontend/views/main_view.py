import tkinter as tk
from tkinter import ttk, messagebox
from controllers.note_controller import NoteController
from views.add_note_view import AddNoteWindow

class MainAppWindow(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.title("Smart Note - Quản lý Ghi chú")
        self.geometry("780x520")
        self.configure(bg="#F5F7FB")
        self.resizable(False, False)
        self.note_controller = NoteController()
        self.note_map = {}
        self.selected_note_id = None
        self.edit_window_open = False

        self.style = ttk.Style(self)
        self.style.theme_use("clam")
        self.style.configure("Treeview.Heading", background="#1976D2", foreground="white", font=("Arial", 10, "bold"))
        self.style.configure("Treeview", rowheight=28, font=("Arial", 10), fieldbackground="#F7FAFF", background="#FFFFFF", bordercolor="#E0E0E0", relief="flat")
        self.style.map("Treeview", background=[("selected", "#BBDEFB")], foreground=[("selected", "black")])
        self.style.configure("Accent.TButton", background="#0288D1", foreground="white", font=("Arial", 10, "bold"))
        self.style.configure("Secondary.TButton", background="#E0E0E0", foreground="#333333", font=("Arial", 10))

        header_frame = tk.Frame(self, bg="#ffffff", bd=0, relief="flat")
        header_frame.pack(fill="x", padx=15, pady=(15, 5))
        tk.Label(header_frame, text="Smart Note", fg="#2E3A59", bg="#ffffff", font=("Arial", 16, "bold")).pack(side="left")
        tk.Label(header_frame, text=f"👤 Xin chào: {user.fullname}", fg="#666666", bg="#ffffff", font=("Arial", 10, "italic")).pack(side="right")

        subtitle = tk.Label(self, text="Chọn ghi chú để cập nhật. Double-click vào một dòng hoặc chọn và nhấn nút Sửa.", fg="#555555", bg="#F5F7FB", font=("Arial", 9))
        subtitle.pack(anchor="w", padx=18)

        content_frame = tk.Frame(self, bg="#F5F7FB")
        content_frame.pack(fill="both", expand=True, padx=15, pady=10)

        # Bảng danh sách ghi chú
        frame_list = tk.Frame(content_frame, bg="#F5F7FB")
        frame_list.pack(side="left", fill="both", expand=True)

        columns = ("title", "category", "priority", "create_at")
        self.tree = ttk.Treeview(frame_list, columns=columns, show="headings", height=12)
        self.tree.heading("title", text="Tiêu đề")
        self.tree.heading("category", text="Chủ đề")
        self.tree.heading("priority", text="Mức độ")
        self.tree.heading("create_at", text="Ngày tạo")
        
        self.tree.column("title", width=300)
        self.tree.column("category", width=100, anchor="center")
        self.tree.column("priority", width=100, anchor="center")
        self.tree.column("create_at", width=100, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)
        self.tree.bind("<Double-1>", self.on_row_double_click)

        scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        detail_frame = ttk.LabelFrame(content_frame, text="Thông tin ghi chú", padding=(12, 12))
        detail_frame.pack(side="right", fill="y", padx=(15, 0), pady=0)
        detail_frame.configure(width=240)

        self.note_title_label = tk.Label(detail_frame, text="Tiêu đề: ", anchor="w", justify="left", font=("Arial", 10, "bold"))
        self.note_title_label.pack(fill="x", pady=(0, 4))
        self.note_category_label = tk.Label(detail_frame, text="Chủ đề: ", anchor="w", justify="left", font=("Arial", 10))
        self.note_category_label.pack(fill="x", pady=(0, 4))
        self.note_priority_label = tk.Label(detail_frame, text="Mức độ: ", anchor="w", justify="left", font=("Arial", 10))
        self.note_priority_label.pack(fill="x", pady=(0, 4))
        self.note_create_at_label = tk.Label(detail_frame, text="Ngày tạo: ", anchor="w", justify="left", font=("Arial", 10))
        self.note_create_at_label.pack(fill="x", pady=(0, 6))
        self.note_preview = tk.Label(detail_frame, text="Nội dung:", anchor="nw", justify="left", wraplength=200, font=("Arial", 10), fg="#333333")
        self.note_preview.pack(fill="x", pady=(0, 8))
        self.info_label = tk.Label(detail_frame, text="Chọn ghi chú để xem trước hoặc sửa.", fg="#777777", wraplength=220, justify="left", font=("Arial", 9))
        self.info_label.pack(fill="x")

        # Nút bấm chức năng
        frame_btn = tk.Frame(self, bg="#F5F7FB")
        frame_btn.pack(fill="x", padx=15, pady=15)
        tk.Button(frame_btn, text="+ Thêm Ghi Chú", bg="#0288D1", fg="white", font=("Arial", 10, "bold"), command=self.open_add_note, relief="flat", padx=12, pady=8).pack(side="left")
        tk.Button(frame_btn, text="✏️ Sửa Ghi Chú", bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.open_selected_note, relief="flat", padx=12, pady=8).pack(side="left", padx=10)
        tk.Button(frame_btn, text="🔄 Tải lại", bg="#E0E0E0", fg="#333333", font=("Arial", 10), command=self.load_data, relief="flat", padx=12, pady=8).pack(side="left")

        # Khởi chạy tải dữ liệu
        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        self.note_map = {}
        self.selected_note_id = None
        self.update_detail_panel(None)
        success, data = self.note_controller.get_notes()
        if success:
            for index, note in enumerate(data):
                note_id = str(note.id)
                self.note_map[note_id] = note
                row_tag = "evenrow" if index % 2 == 0 else "oddrow"
                self.tree.insert("", "end", iid=note_id, values=(note.title, note.category, note.priority, note.create_at), tags=(row_tag,))
            self.tree.tag_configure("evenrow", background="#FFFFFF")
            self.tree.tag_configure("oddrow", background="#F3F7FF")
        else:
            messagebox.showerror("Lỗi", data)

    def update_detail_panel(self, note):
        if note is None:
            self.note_title_label.config(text="Tiêu đề: ")
            self.note_category_label.config(text="Chủ đề: ")
            self.note_priority_label.config(text="Mức độ: ")
            self.note_create_at_label.config(text="Ngày tạo: ")
            self.note_preview.config(text="Nội dung:")
            self.info_label.config(text="Chọn một ghi chú để xem trước hoặc sửa.")
            return

        self.note_title_label.config(text=f"Tiêu đề: {note.title}")
        self.note_category_label.config(text=f"Chủ đề: {note.category}")
        self.note_priority_label.config(text=f"Mức độ: {note.priority}")
        self.note_create_at_label.config(text=f"Ngày tạo: {note.create_at}")
        self.note_preview.config(text=f"Nội dung: {note.content[:150]}{'...' if len(note.content) > 150 else ''}")
        self.info_label.config(text="Nhấn nút Sửa Ghi Chú hoặc nháy đúp để chỉnh sửa.")

    def on_tree_select(self, event=None):
        selection = self.tree.selection()
        if not selection:
            return

        item_id = selection[0]
        self.selected_note_id = item_id
        note = self.note_map.get(item_id)
        self.update_detail_panel(note)

    def on_row_double_click(self, event=None):
        self.open_selected_note()

    def open_selected_note(self):
        if self.edit_window_open:
            return

        if not self.selected_note_id:
            messagebox.showwarning("Chú ý", "Vui lòng chọn ghi chú trước khi sửa.")
            return

        note = self.note_map.get(self.selected_note_id)
        if not note:
            messagebox.showerror("Lỗi", "Không tìm thấy ghi chú đã chọn.")
            return

        self.edit_window_open = True
        edit_window = AddNoteWindow(self, note_data=note)
        self.wait_window(edit_window)
        self.edit_window_open = False
        self.load_data()

    def open_add_note(self):
        add_window = AddNoteWindow(self)
        self.wait_window(add_window)
        self.load_data() # Tự động load lại sau khi thêm xong