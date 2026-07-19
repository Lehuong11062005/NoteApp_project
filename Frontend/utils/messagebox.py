from tkinter import messagebox

def show_success(title, message):
    messagebox.showinfo(title, message)

def show_error(title, message):
    messagebox.showerror(title, message)