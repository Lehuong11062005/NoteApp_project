import sys
import os

# Thêm đường dẫn gốc để Python nhận diện các package
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox
from Frontend.services.api_client import APIClient
from Frontend.views.login_view import LoginView  # <--- Import màn hình Đăng nhập

def launch_app():
    # 1. Kiểm tra kết nối tới Backend trước khi mở app
    is_alive, data = APIClient.check_server()
    
    if not is_alive:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Lỗi Kết Nối", data)
        root.destroy()
        return

    # 2. Khởi động ứng dụng bằng màn hình Đăng nhập
    app = LoginView()
    app.mainloop()

if __name__ == "__main__":
    launch_app()