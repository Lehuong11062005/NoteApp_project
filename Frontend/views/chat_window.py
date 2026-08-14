import threading
import tkinter as tk
from tkinter import scrolledtext, ttk
from Frontend.controllers.chat_controller import ChatController


class ChatbotWindow(tk.Toplevel):

  def __init__(self, parent, user_id="guest"):
    super().__init__(parent)
    self.user_id = user_id
    self.chat_controller = ChatController()  # 🟢 Khởi tạo Controller thật

    self.title("🤖 Trợ Lý AI - Smart Note")
    self.geometry("480x580")
    self.configure(bg="#F5F7FB")
    self.grab_set()

    self._build_ui()
    self._append_message(
        "Trợ lý AI",
        "Xin chào! Tôi có thể giúp gì cho bạn với các ghi chú hôm nay?",
    )

  def _build_ui(self):
    self.chat_area = scrolledtext.ScrolledText(
        self, wrap="word", font=("Arial", 10), state="disabled", bg="#FFFFFF"
    )
    self.chat_area.pack(fill="both", expand=True, padx=12, pady=12)

    input_frame = tk.Frame(self, bg="#F5F7FB")
    input_frame.pack(fill="x", padx=12, pady=(0, 12))

    self.entry_msg = ttk.Entry(input_frame, font=("Arial", 10))
    self.entry_msg.pack(side="left", fill="x", expand=True, padx=(0, 8))
    self.entry_msg.bind("<Return>", lambda event: self.send_message())

    self.btn_send = tk.Button(
        input_frame,
        text="Gửi 🚀",
        bg="#1976D2",
        fg="white",
        font=("Arial", 9, "bold"),
        relief="flat",
        cursor="hand2",
        command=self.send_message,
    )
    self.btn_send.pack(side="right")

  def send_message(self):
    msg = self.entry_msg.get().strip()
    if not msg:
      return

    self._append_message("Bạn", msg)
    self.entry_msg.delete(0, tk.END)
    self.btn_send.config(state="disabled", text="Đang nghĩ...")

    # Chạy luồng ngầm để gọi Controller thật (UI không bị đơ)
    threading.Thread(
        target=self._process_reply_real, args=(msg,), daemon=True
    ).start()

  def _process_reply_real(self, msg):
    # 🟢 GỌI CONTROLLER THẬT
    success, reply = self.chat_controller.ask_chatbot(self.user_id, msg)

    if not success:
      reply = f"❌ {reply}"

    # Cập nhật kết quả lên UI
    self.after(0, lambda: self._on_receive_reply(reply))

  def _on_receive_reply(self, reply):
    self._append_message("Trợ lý AI", reply)
    self.btn_send.config(state="normal", text="Gửi 🚀")

  def _append_message(self, sender, text):
    self.chat_area.config(state="normal")
    tag_name = "user_tag" if sender == "Bạn" else "bot_tag"
    self.chat_area.insert(tk.END, f"{sender}: ", tag_name)
    self.chat_area.insert(tk.END, f"{text}\n\n")
    self.chat_area.tag_config(
        "user_tag", foreground="#1976D2", font=("Arial", 10, "bold")
    )
    self.chat_area.tag_config(
        "bot_tag", foreground="#00897B", font=("Arial", 10, "bold")
    )
    self.chat_area.config(state="disabled")
    self.chat_area.see(tk.END)