import tkinter as tk
from tkinter import filedialog

def choose_image_file() -> str:
    """
    Hiển thị dialog chọn file ảnh từ hệ thống.
    Trả về đường dẫn tới file đã chọn hoặc chuỗi rỗng nếu hủy chọn.
    """
    filetypes = (
        ("Tệp hình ảnh", "*.png *.jpg *.jpeg *.gif *.webp"),
        ("Tất cả tệp", "*.*")
    )
    filepath = filedialog.askopenfilename(
        title="Chọn ảnh đính kèm",
        filetypes=filetypes
    )
    return filepath or ""
