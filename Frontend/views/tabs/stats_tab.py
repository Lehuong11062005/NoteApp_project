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

        self.stats_figure = Figure(figsize=(6, 4), dpi=100)
        self.stats_canvas = FigureCanvasTkAgg(self.stats_figure, master=self)
        self.stats_canvas.get_tk_widget().pack(fill="both", expand=True)

    def load_statistics(self):
        period = "month" if self.period_var.get() == "Tháng" else "day"
        success, data = self.note_controller.get_statistics(period)
        if not success:
            return

        self.stats_figure.clear()
        axes = self.stats_figure.add_subplot(111)
        
        if not data:
            axes.text(0.5, 0.5, "Chưa có ghi chú để thống kê", ha="center", va="center")
            axes.axis("off")
        else:
            dates = [item[0] for item in data]
            counts = [item[1] for item in data]
            axes.bar(dates, counts, color="#1976D2", width=0.7)
            axes.set_xlabel("Tháng" if period == "month" else "Ngày")
            axes.set_ylabel("Số lượng ghi chú")
            axes.set_title("Năng suất làm việc theo thời gian")
            axes.tick_params(axis="x", rotation=0, pad=8)
            axes.grid(axis="y", alpha=0.25)
            
        self.stats_figure.tight_layout()
        self.stats_canvas.draw()