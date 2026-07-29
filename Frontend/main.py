import tkinter as tk
from tkinter import messagebox
from services.api_client import APIClient
from views.login_view import LoginWindow
from views.main_view import MainAppWindow

def start_main_app(user):
    # Khởi chạy màn hình chính với thông tin user vừa đăng nhập
    def on_logout():
        app.destroy()
        launch()  # Mở lại màn hình Login

    app = MainAppWindow(user, on_logout_callback=on_logout)
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