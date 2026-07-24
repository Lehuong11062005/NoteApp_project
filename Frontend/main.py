import sys
import os

# Ép Python nhận diện thư mục Frontend làm gốc
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import tkinter as tk
from tkinter import messagebox
from services.api_client import APIClient

# Import thẳng form Đăng ký của chúng ta vào đây
from views.register_view import RegisterView

def launch_app():
    # 1. Kiểm tra kết nối Backend trước khi bật app
    is_alive, data = APIClient.check_server()
    
    if not is_alive:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Lỗi Kết Nối", data)
        root.destroy()
        return

    # 2. Khởi chạy trực tiếp Màn hình Đăng ký làm cửa sổ chính
    app = RegisterView()
    app.mainloop()

if __name__ == "__main__":
    launch_app()