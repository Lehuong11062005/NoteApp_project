# frontend/main.py
import tkinter as tk
from tkinter import messagebox
from services.api_client import APIClient

def launch_app():
    # 1. Kiểm tra kết nối tới Backend trước khi mở giao diện
    is_alive, data = APIClient.check_server()
    
    if not is_alive:
        # Nếu backend chưa bật, hiện thông báo lỗi và đóng ứng dụng ngay
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Lỗi Kết Nối", data)
        root.destroy()
        return

    # 2. Mở màn hình đăng nhập nếu kết nối thông suốt
    from Frontend.views.login_view import LoginView
    app = LoginView()
    app.mainloop()

if __name__ == "__main__":
    launch_app()