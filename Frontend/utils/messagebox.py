from tkinter import messagebox

def show_success(title: str, message: str):
    messagebox.showinfo(title, message)

def show_error(title: str, message: str):
    messagebox.showerror(title, message)