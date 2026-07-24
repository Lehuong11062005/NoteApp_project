import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import tkinter as tk
from tkinter import messagebox
from Frontend.services.api_client import APIClient
from Frontend.views.login_view import LoginView  

def launch_app():
    is_alive, data = APIClient.check_server()
    
    if not is_alive:
        root = tk.Tk()
        root.withdraw()
        messagebox.showerror("Lỗi Kết Nối", data)
        root.destroy()
        return

    app = LoginView()
    app.mainloop()

if __name__ == "__main__":
    launch_app()