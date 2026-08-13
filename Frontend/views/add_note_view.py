import sys
import threading
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry

try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

try:
    import speech_recognition as sr
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from Frontend.controllers.note_controller import NoteController
from Frontend.utils.file_helper import choose_image_file
from Frontend.services.upload_api import UploadAPI


class AddNoteWindow(tk.Toplevel):
    def __init__(self, parent, note_data=None):
        super().__init__(parent)
        self.note_controller = NoteController()
        self.note_data = note_data
        self.note_id = getattr(note_data, "id", None) if note_data else None
        self.edit_mode = self.note_id is not None
        self.uploaded_image_url = getattr(note_data, "image_url", None) if self.edit_mode else None
        self._photo_ref = None  # giữ reference để tránh Garbage Collector

        self.title("Cập nhật Ghi Chú" if self.edit_mode else "Thêm Ghi Chú Mới")
        self.geometry("520x730")
        self.grab_set()

        # ------------------------------------------
        # 1. TIÊU ĐỀ
        # ------------------------------------------
        tk.Label(self, text="Tiêu đề:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=(10, 0))
        self.entry_title = tk.Entry(self, width=60, font=("Arial", 10))
        self.entry_title.pack(padx=10, pady=2)

        # ------------------------------------------
        # 2. CHỦ ĐỀ & MỨC ĐỘ
        # ------------------------------------------
        frame_row1 = tk.Frame(self)
        frame_row1.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_row1, text="Chủ đề:").pack(side="left")
        self.cb_category = ttk.Combobox(frame_row1, values=["Học tập", "Công việc", "Cá nhân", "Chung"], width=15)
        self.cb_category.current(3)
        self.cb_category.pack(side="left", padx=(5, 15))

        tk.Label(frame_row1, text="Mức độ:").pack(side="left")
        self.cb_priority = ttk.Combobox(frame_row1, values=["Thấp", "Bình Thường", "Cao"], width=15)
        self.cb_priority.current(1)
        self.cb_priority.pack(side="left", padx=5)

        # ------------------------------------------
        # 3. THỜI GIAN NHẮC NHỞ
        # ------------------------------------------
        self.use_reminder_var = tk.BooleanVar(value=False)
        tk.Checkbutton(
            self, text="Bật nhắc nhở (Chọn ngày giờ)",
            variable=self.use_reminder_var,
            command=self.toggle_reminder
        ).pack(anchor="w", padx=5, pady=(5, 0))

        self.reminder_container = tk.Frame(self)
        self.reminder_container.pack(fill="x", padx=10, pady=2)

        self.frame_time = tk.Frame(self.reminder_container)

        self.cal_date = DateEntry(
            self.frame_time, width=12, background='#1976D2',
            foreground='white', borderwidth=2, date_pattern='yyyy-mm-dd'
        )
        self.cal_date.pack(side="left", padx=(0, 15))

        tk.Label(self.frame_time, text="Giờ:").pack(side="left")
        self.spin_hour = ttk.Spinbox(self.frame_time, from_=0, to=23, width=3, format="%02.0f")
        self.spin_hour.set("08")
        self.spin_hour.pack(side="left", padx=(2, 10))

        tk.Label(self.frame_time, text="Phút:").pack(side="left")
        self.spin_minute = ttk.Spinbox(self.frame_time, from_=0, to=59, width=3, format="%02.0f")
        self.spin_minute.set("00")
        self.spin_minute.pack(side="left", padx=(2, 0))

        self.toggle_reminder()

        # ------------------------------------------
        # 4. ĐÍNH KÈM ẢNH
        # ------------------------------------------
        frame_img_box = tk.LabelFrame(self, text="Ảnh đính kèm", font=("Arial", 9, "bold"), fg="#333333")
        frame_img_box.pack(fill="x", padx=10, pady=5)

        frame_img_actions = tk.Frame(frame_img_box)
        frame_img_actions.pack(fill="x", padx=5, pady=2)

        self.btn_select_img = tk.Button(
            frame_img_actions, text="📷 Chọn ảnh...", bg="#1976D2", fg="white",
            font=("Arial", 9, "bold"), relief="flat", cursor="hand2", command=self.on_choose_image
        )
        self.btn_select_img.pack(side="left", padx=(0, 10))

        self.btn_clear_img = tk.Button(
            frame_img_actions, text="❌ Xóa ảnh", bg="#E53935", fg="white",
            font=("Arial", 9), relief="flat", cursor="hand2", command=self.on_clear_image
        )
        self.btn_clear_img.pack(side="left")

        self.lbl_img_status = tk.Label(frame_img_box, text="Chưa có ảnh nào", fg="#666666", anchor="w", wraplength=480)
        self.lbl_img_status.pack(fill="x", padx=5, pady=(2, 5))

        self.lbl_img_preview = tk.Label(frame_img_box, bg="#f0f0f0", relief="flat")

        if self.uploaded_image_url:
            self.lbl_img_status.config(text="✓ Đã có ảnh đính kèm", fg="#2E7D32")
            self._load_image_from_url(self.uploaded_image_url)
        else:
            self.btn_clear_img.pack_forget()

        # ------------------------------------------
        # 5. TRẠNG THÁI (Chỉ hiển thị khi Sửa)
        # ------------------------------------------
        if self.edit_mode:
            tk.Label(self, text="Trạng thái:").pack(anchor="w", padx=10, pady=(5, 0))
            self.cb_status = ttk.Combobox(self, values=["Đang chờ", "Đã hoàn thành", "Quá hạn"], width=57)
            self.cb_status.pack(padx=10, pady=2)

            current_status = getattr(note_data, "status", "Đang chờ")
            self.cb_status.set(current_status)

        # ------------------------------------------
        # 6. NỘI DUNG & NÚT VOICE-TO-TEXT
        # ------------------------------------------
        frame_content_header = tk.Frame(self)
        frame_content_header.pack(fill="x", padx=10, pady=(5, 0))

        tk.Label(frame_content_header, text="Nội dung:", font=("Arial", 10, "bold")).pack(side="left")

        self.btn_voice = tk.Button(
            frame_content_header, text="🎙️ Nhập bằng giọng nói", bg="#00897B", fg="white",
            font=("Arial", 8, "bold"), relief="flat", cursor="hand2", command=self.start_voice_input
        )
        self.btn_voice.pack(side="right")

        self.txt_content = tk.Text(self, height=7, width=60, font=("Arial", 10))
        self.txt_content.pack(padx=10, pady=2)

        self.lbl_voice_status = tk.Label(self, text="", fg="gray", font=("Arial", 8, "italic"))
        self.lbl_voice_status.pack(anchor="w", padx=10)

        # ------------------------------------------
        # 7. NẠP DỮ LIỆU CŨ NẾU LÀ CHẾ ĐỘ SỬA
        # ------------------------------------------
        if self.edit_mode:
            self.entry_title.insert(0, getattr(note_data, "title", ""))
            self.cb_category.set(getattr(note_data, "category", "Chung"))
            self.cb_priority.set(getattr(note_data, "priority", "Bình Thường"))
            self.txt_content.insert("1.0", getattr(note_data, "content", ""))

            reminder = getattr(note_data, "reminder_time", "")
            if reminder and len(str(reminder)) >= 16:
                self.use_reminder_var.set(True)
                self.toggle_reminder()

                reminder_str = str(reminder)
                date_part = reminder_str[:10]
                time_part = reminder_str[11:16]
                hour_part, min_part = time_part.split(":")

                self.cal_date.set_date(date_part)
                self.spin_hour.set(hour_part)
                self.spin_minute.set(min_part)

        # ------------------------------------------
        # 8. NÚT LƯU GHI CHÚ
        # ------------------------------------------
        self.btn_save = tk.Button(
            self, text="Cập nhật" if self.edit_mode else "Lưu Ghi Chú",
            bg="#4CAF50", fg="white", font=("Arial", 10, "bold"), command=self.save_note,
            padx=15, pady=5, cursor="hand2"
        )
        self.btn_save.pack(pady=10)

    # ==========================================
    # CÁC PHƯƠNG THỨC XỬ LÝ (METHODS)
    # ==========================================

    def toggle_reminder(self):
        if self.use_reminder_var.get():
            self.frame_time.pack(fill="x")
        else:
            self.frame_time.pack_forget()

    # --- HÀM CHỌN ẢNH & UPLOAD ẢNH ---
    def on_choose_image(self):
        filepath = choose_image_file()
        if not filepath:
            return

        import os
        filename = os.path.basename(filepath)
        self.lbl_img_status.config(text=f"⏳ Đang tải '{filename}' lên...", fg="#E65100")
        self.btn_select_img.config(state="disabled")
        self.update_idletasks()

        self._show_local_preview(filepath)

        def _do_upload():
            success, res = UploadAPI.upload_image(filepath)
            self.after(0, lambda: self._on_upload_done(success, res))

        threading.Thread(target=_do_upload, daemon=True).start()

    def _on_upload_done(self, success: bool, res: str):
        self.btn_select_img.config(state="normal")
        if success:
            self.uploaded_image_url = res
            self.lbl_img_status.config(text="✓ Đã đính kèm ảnh", fg="#2E7D32")
            self.btn_clear_img.pack(side="left")
        else:
            self.lbl_img_status.config(text=f"❌ {res}", fg="#C62828")
            self.lbl_img_preview.pack_forget()
            messagebox.showerror("Lỗi tải ảnh", f"Không thể upload ảnh:\n{res}")

    def on_clear_image(self):
        self.uploaded_image_url = None
        self._photo_ref = None
        self.lbl_img_status.config(text="Chưa có ảnh nào", fg="#666666")
        self.lbl_img_preview.config(image="")
        self.lbl_img_preview.pack_forget()
        self.btn_clear_img.pack_forget()

    def _show_local_preview(self, filepath: str):
        if not PIL_AVAILABLE:
            return
        try:
            img = Image.open(filepath)
            img.thumbnail((200, 150), Image.LANCZOS)
            self._show_preview(img)
        except Exception:
            pass

    def _show_preview(self, img):
        photo = ImageTk.PhotoImage(img)
        self._photo_ref = photo
        self.lbl_img_preview.config(image=photo)
        self.lbl_img_preview.pack(padx=5, pady=(0, 5))

    def _load_image_from_url(self, url: str):
        if not PIL_AVAILABLE or not url:
            return

        def _fetch():
            try:
                import urllib.request
                import io
                with urllib.request.urlopen(url, timeout=5) as resp:
                    data = resp.read()
                img = Image.open(io.BytesIO(data))
                img.thumbnail((200, 150), Image.LANCZOS)
                self.after(0, lambda: self._show_preview(img))
            except Exception:
                pass

        threading.Thread(target=_fetch, daemon=True).start()

    # --- HÀM VOICE-TO-TEXT ---
    def start_voice_input(self):
        if not SPEECH_AVAILABLE:
            messagebox.showerror("Thiếu thư viện", "Chưa cài đặt 'SpeechRecognition' hoặc 'PyAudio'.\nHãy chạy: pip install SpeechRecognition PyAudio")
            return

        self.btn_voice.config(state="disabled", bg="#B0BEC5")
        self.lbl_voice_status.config(text="🔴 Đang nghe... Hãy nói vào Micro!", fg="#D32F2F")

        threading.Thread(target=self._process_speech, daemon=True).start()

    def _process_speech(self):
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                text = recognizer.recognize_google(audio, language="vi-VN")
                
                self.after(0, lambda: self._on_speech_success(text))
        except sr.WaitTimeoutError:
            self.after(0, lambda: self._on_speech_error("Hết thời gian chờ (Không nghe thấy tiếng)."))
        except sr.UnknownValueError:
            self.after(0, lambda: self._on_speech_error("Không thể nhận diện giọng nói."))
        except sr.RequestError:
            self.after(0, lambda: self._on_speech_error("Lỗi kết nối mạng (Cần Internet)."))
        except Exception as e:
            self.after(0, lambda: self._on_speech_error(f"Lỗi Mic: {str(e)}"))

    def _on_speech_success(self, text):
        self.txt_content.insert(tk.INSERT, f"{text} ")
        self.lbl_voice_status.config(text="✅ Nhận diện thành công!", fg="#2E7D32")
        self.btn_voice.config(state="normal", bg="#00897B")

    def _on_speech_error(self, error_msg):
        self.lbl_voice_status.config(text=f"❌ {error_msg}", fg="#D32F2F")
        self.btn_voice.config(state="normal", bg="#00897B")

    # --- HÀM LƯU GHI CHÚ ---
    def save_note(self):
        title = self.entry_title.get().strip()
        content = self.txt_content.get("1.0", tk.END).strip()
        category = self.cb_category.get()
        priority = self.cb_priority.get()
        image_url = self.uploaded_image_url

        reminder_time = None
        if self.use_reminder_var.get():
            date_val = self.cal_date.get()
            hour_val = self.spin_hour.get().zfill(2)
            minute_val = self.spin_minute.get().zfill(2)
            reminder_time = f"{date_val} {hour_val}:{minute_val}"

        if self.edit_mode:
            status = self.cb_status.get()
            success, msg = self.note_controller.update_note(
                note_id=self.note_id, title=title, content=content,
                category=category, priority=priority,
                reminder_time=reminder_time, image_url=image_url, status=status
            )
        else:
            success, msg = self.note_controller.create_note(
                title=title, content=content, category=category, priority=priority,
                reminder_time=reminder_time, image_url=image_url
            )

        if success:
            messagebox.showinfo("Thành công", msg)
            self.destroy()
        else:
            messagebox.showerror("Lỗi", msg)