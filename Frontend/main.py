import sys
import os
import tkinter as tk
from tkinter import messagebox

# Thêm thư mục gốc vào path để import các modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Frontend.services.api_client import APIClient
from Frontend.views.login_view import LoginView

def launch_app():
    # 1. Kiểm tra kết nối tới Backend trước khi mở ứng dụng
    is_alive, data = APIClient.check_server()
    
    if not is_alive:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Lỗi Kết Nối", f"Không thể kết nối đến máy chủ Backend!\nChi tiết: {data}")
        root.destroy()
        return

    # 2. Khởi chạy màn hình LoginView (Form Đăng nhập)
    app = LoginView()
    app.mainloop()

if __name__ == "__main__":
    launch_app()