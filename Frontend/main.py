# Frontend/main.py
import tkinter as tk
from tkinter import messagebox
from services.api_client import APIClient
from views.add_note_view import AddNoteWindow  # Import giao diện thêm ghi chú

def open_add_note(window):
    """Hàm mở cửa sổ thêm ghi chú mới"""
    add_window = AddNoteWindow(window)
    add_window.grab_set()  # Giữ tập trung vào cửa sổ thêm ghi chú

def launch_app():
    # 1. Kiểm tra kết nối tới Backend
    is_alive, data = APIClient.check_server()
    
    if not is_alive:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Lỗi Kết Nối", data)
        root.destroy()
        return

    # 2. Khởi tạo màn hình chính của Ứng dụng
    window = tk.Tk()
    window.title("Ứng dụng Ghi chú Cá nhân")
    window.geometry("400x200")

    # Hiển thị trạng thái kết nối
    lbl_status = tk.Label(window, text=f"✅ {data}", fg="green", font=("Arial", 10, "bold"))
    lbl_status.pack(pady=10)

    # Nút bấm để test chức năng Thêm Ghi Chú
    btn_add = tk.Button(
        window, 
        text="+ Thêm Ghi Chú Mới", 
        bg="#0288D1", 
        fg="white", 
        font=("Arial", 11, "bold"),
        padx=10, 
        pady=5,
        command=lambda: open_add_note(window)
    )
    btn_add.pack(pady=20)
    
    window.mainloop()

if __name__ == "__main__":
    launch_app()