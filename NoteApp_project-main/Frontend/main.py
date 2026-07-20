import tkinter as tk
from Frontend.controllers.auth_controller import AuthController

def launch_app():
    # Khởi tạo cửa sổ giao diện Tkinter
    window = tk.Tk()
    window.title("Note App - Đăng ký tài khoản")
    window.geometry("360x340")
    
    # Khởi chạy bộ điều khiển Đăng ký
    auth_controller = AuthController(window)
    
    window.mainloop()

if __name__ == "__main__":
    launch_app()