import os
import requests
from dotenv import load_dotenv
from tkinter import messagebox  # Bổ sung import messagebox

load_dotenv()

BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")

class AuthController:
    def __init__(self, view):
        self.view = view

    def handle_register(self):
        data = self.view.get_register_data()

        url = f"{BASE_URL}/auth/register"
        try:
            response = requests.post(url, json=data)
            
            # Kiểm tra phản hồi từ Backend
            if response.status_code in [200, 201]:
                messagebox.showinfo("Thành công", "Đăng ký tài khoản thành công!")
                if hasattr(self.view, 'destroy'):
                    self.view.destroy()  # Đóng cửa sổ đăng ký sau khi thành công
            else:
                # Lấy câu thông báo lỗi từ backend (nếu có)
                err_data = response.json()
                detail = err_data.get("detail", "Đăng ký không thành công!")
                messagebox.showerror("Thất bại", f"Lỗi: {detail}")
                
        except Exception as e:
            print("Lỗi kết nối:", e)
            messagebox.showerror("Lỗi kết nối", f"Không thể kết nối đến server:\n{e}")