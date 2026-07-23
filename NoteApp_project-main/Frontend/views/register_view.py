import tkinter as tk
from tkinter import messagebox
from Frontend.services.api_client import call_register_api
class RegisterWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Đăng ký tài khoản")
        self.root.geometry("350x250")
        self.root.resizable(False, False)
        
        # Tiêu đề form
        title_label = tk.Label(root, text="ĐĂNG KÝ", font=("Arial", 16, "bold"))
        title_label.pack(pady=15)
        
        # Khung nhập Username
        tk.Label(root, text="Tên đăng nhập:").pack(anchor="w", padx=40)
        self.username_entry = tk.Entry(root, width=35)
        self.username_entry.pack(pady=5)
        
        # Khung nhập Password
        tk.Label(root, text="Mật khẩu:").pack(anchor="w", padx=40)
        self.password_entry = tk.Entry(root, width=35, show="*") # Ẩn mật khẩu bằng dấu *
        self.password_entry.pack(pady=5)
        
        # Nút Đăng ký
        self.register_btn = tk.Button(root, text="Đăng ký", command=self.handle_register, bg="#4CAF50", fg="white", width=15)
        self.register_btn.pack(pady=20)

    def handle_register(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # Kiểm tra nhanh dữ liệu rỗng ở client
        if not username or not password:
            messagebox.showwarning("Chú ý", "Vui lòng nhập đầy đủ thông tin!")
            return
            
        if len(password) < 6:
            messagebox.showwarning("Chú ý", "Mật khẩu phải có ít nhất 6 ký tự!")
            return

        # Gọi API
        status_code, result = call_register_api(username, password)
        
        if status_code == 200:
            messagebox.showinfo("Thành công", result.get("message"))
            # Xóa trắng form sau khi đăng ký thành công
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            # Lấy thông báo lỗi từ backend trả về
            error_msg = result.get("detail", "Đã có lỗi xảy ra.")
            messagebox.showerror("Thất bại", error_msg)

# Đoạn code dùng để chạy thử độc lập giao diện
if __name__ == "__main__":
    main_root = tk.Tk()
    app = RegisterWindow(main_root)
    main_root.mainloop()