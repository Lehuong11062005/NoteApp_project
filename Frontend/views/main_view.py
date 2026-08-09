import sys
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Frontend.controllers.note_controller import NoteController
from Frontend.views.add_note_view import AddNoteWindow

class MainAppWindow(tk.Tk):
    def __init__(self, user):
        super().__init__()
        self.title("Smart Note - Quản lý Ghi chú")
        self.geometry("700x450")
        self.note_controller = NoteController(user.username)

        # Thanh tiêu đề (Header)
        tk.Label(self, text=f"👤 Xin chào: {user.fullname}", fg="gray", font=("Arial", 10, "italic")).pack(anchor="w", padx=15, pady=5)
        
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=15, pady=5)

        notes_tab = ttk.Frame(notebook)
        stats_tab = ttk.Frame(notebook)
        notebook.add(notes_tab, text="Danh sách ghi chú")
        notebook.add(stats_tab, text="Thống kê")

        # Bảng danh sách ghi chú
        frame_list = tk.Frame(notes_tab)
        frame_list.pack(fill="both", expand=True, padx=5, pady=5)

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

        scrollbar = ttk.Scrollbar(frame_list, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Nút bấm chức năng
        frame_btn = tk.Frame(notes_tab)
        frame_btn.pack(fill="x", padx=5, pady=10)
        tk.Button(frame_btn, text="+ Thêm Ghi Chú", bg="#0288D1", fg="white", font=("Arial", 10, "bold"), command=self.open_add_note).pack(side="left")
        tk.Button(frame_btn, text="🔄 Tải lại", command=self.load_data).pack(side="left", padx=10)

        self.stats_figure = Figure(figsize=(6, 4), dpi=100)
        self.stats_canvas = FigureCanvasTkAgg(self.stats_figure, master=stats_tab)
        self.stats_canvas.get_tk_widget().pack(fill="both", expand=True)

        # Khởi chạy tải dữ liệu
        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
            
        success, data = self.note_controller.get_notes()
        if success:
            for note in data:
                self.tree.insert("", "end", values=(note.title, note.category, note.priority, note.create_at))
        else:
            messagebox.showerror("Lỗi", data)

        self.load_statistics()

    def load_statistics(self):
        success, data = self.note_controller.get_statistics()
        if not success:
            messagebox.showerror("Lỗi", data)
            return

        self.stats_figure.clear()
        axes = self.stats_figure.add_subplot(111)
        if not data:
            axes.text(0.5, 0.5, "Chưa có ghi chú để thống kê", ha="center", va="center")
            axes.axis("off")
        else:
            categories = [item[0] for item in data]
            counts = [item[1] for item in data]
            color_map = {
                "Học tập": "#1976D2",
                "Công việc": "#F57C00",
                "Cá nhân": "#388E3C",
                "Chung": "#757575",
            }
            fallback_colors = ["#7B1FA2", "#0097A7", "#C2185B", "#AFB42B"]
            colors = [
                color_map.get(category, fallback_colors[index % len(fallback_colors)])
                for index, category in enumerate(categories)
            ]
            axes.pie(
                counts,
                labels=categories,
                colors=colors,
                autopct="%1.1f%%",
                startangle=90,
            )
            axes.set_title("Tỷ lệ ghi chú theo chủ đề")
            axes.axis("equal")
        self.stats_figure.tight_layout()
        self.stats_canvas.draw()

    def open_add_note(self):
        add_window = AddNoteWindow(self)
        self.wait_window(add_window)
        self.load_data() # Tự động load lại sau khi thêm xong