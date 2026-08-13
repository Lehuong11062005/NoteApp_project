import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class StatsTab(ttk.Frame):
    def __init__(self, parent, note_controller):
        super().__init__(parent)
        self.note_controller = note_controller

        stats_controls = tk.Frame(self)
        stats_controls.pack(fill="x", padx=5, pady=5)
        
        tk.Label(stats_controls, text="Khoảng thời gian:").pack(side="left")
        self.period_var = tk.StringVar(value="Ngày")
        period_selector = ttk.Combobox(
            stats_controls, textvariable=self.period_var,
            values=["Ngày", "Tháng"], state="readonly", width=10
        )
        period_selector.pack(side="left", padx=8)
        period_selector.bind("<<ComboboxSelected>>", lambda event: self.load_statistics())

        # ✅ Mở rộng chiều ngang để chứa 2 biểu đồ (Pie và Area)
        self.stats_figure = Figure(figsize=(10, 4), dpi=100)
        self.stats_canvas = FigureCanvasTkAgg(self.stats_figure, master=self)
        self.stats_canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_statistics(self):
        period = "month" if self.period_var.get() == "Tháng" else "day"
        
        # 1. Lấy dữ liệu đếm theo thời gian (Cho biểu đồ Miền)
        success_time, data_time = self.note_controller.get_statistics(period)
        
        # 2. Lấy dữ liệu đếm theo trạng thái (Cho biểu đồ Tròn)
        # Lưu ý: Cần thêm hàm get_statistics_by_status trong note_controller
        success_status, data_status = self.note_controller.get_statistics_by_status() 

        self.stats_figure.clear()
        
        if not success_time or not success_status:
            ax = self.stats_figure.add_subplot(111)
            ax.text(0.5, 0.5, "Lỗi tải dữ liệu", ha="center", va="center")
            ax.axis("off")
            self.stats_canvas.draw()
            return

        # ==========================================
        # BIỂU ĐỒ TRÒN (Trạng thái) - Nửa trái (121)
        # ==========================================
        ax1 = self.stats_figure.add_subplot(121)
        if not data_status:
            ax1.text(0.5, 0.5, "Chưa có dữ liệu", ha="center", va="center")
        else:
            labels = [item[0] for item in data_status] # Tên trạng thái
            sizes = [item[1] for item in data_status]  # Số lượng
            colors = ['#FFCA28' if l=='Đang chờ' else '#4CAF50' if l=='Đã hoàn thành' else '#F44336' for l in labels]
            
            ax1.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
            ax1.set_title("Tỉ lệ Trạng thái")

        # ==========================================
        # BIỂU ĐỒ MIỀN (Thời gian) - Nửa phải (122)
        # ==========================================
        ax2 = self.stats_figure.add_subplot(122)
        if not data_time:
            ax2.text(0.5, 0.5, "Chưa có dữ liệu", ha="center", va="center")
        else:
            dates = [item[0] for item in data_time]
            counts = [item[1] for item in data_time]
            
            # Vẽ kiểu miền (Area chart) bằng fill_between
            ax2.fill_between(dates, counts, color="#64B5F6", alpha=0.4)
            ax2.plot(dates, counts, color="#1976D2", alpha=0.8, linewidth=2, marker='o')
            
            ax2.set_xlabel("Tháng" if period == "month" else "Ngày")
            ax2.set_ylabel("Số lượng công việc")
            ax2.set_title("Biến động công việc")
            ax2.tick_params(axis="x", rotation=45)
            ax2.grid(axis="y", linestyle='--', alpha=0.5)

        self.stats_figure.tight_layout()
        self.stats_canvas.draw()