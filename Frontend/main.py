import tkinter as tk
from tkinter import messagebox
from Frontend.services.api_client import APIClient
from Frontend.views.login_view import LoginWindow
from Frontend.views.main_view import MainAppWindow

def start_main_app(user):
    # Khởi chạy màn hình chính với thông tin user vừa đăng nhập
    app = MainAppWindow(user)
    app.mainloop()

def launch():
    # 1. Kiểm tra kết nối tới Backend trước khi mở App
    is_alive, msg = APIClient.check_server()
    if not is_alive:
        root = tk.Tk()
        root.withdraw() # Ẩn cửa sổ trống
        messagebox.showerror("Lỗi hệ thống", msg)
        root.destroy()
        return

    # 2. Nếu Backend OK, mở màn hình Đăng nhập
    # Truyền hàm start_main_app vào để nó tự mở Ghi chú sau khi Login đúng
    login_app = LoginWindow(on_success_callback=start_main_app)
    login_app.mainloop()

if __name__ == "__main__":
    launch()