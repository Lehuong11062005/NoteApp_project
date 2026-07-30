from services.note_api import NoteAPI
from models.note import Note
from services.upload_api import UploadAPI

class NoteController:
    def __init__(self, view=None):
        self.view = view

    def get_notes(self):
        success, data = NoteAPI.get_all()
        if success:
            notes = []
            for item in data:
                # Chuyển đổi JSON thành Object Note
                create_at = item.get("create_at", "")[:10] if item.get("create_at") else ""
                note = Note(
                    id=item.get("_id"), title=item.get("title", "No Title"),
                    content=item.get("content", ""), category=item.get("category", ""),
                    priority=item.get("priority", ""), create_at=create_at
                )
                notes.append(note)
            return True, notes
        return False, data

    def create_note(self, title, content, category, priority, reminder_time=None, image_url=None):
        if not title or not content:
            return False, "Tiêu đề và nội dung không được để trống!"
        return NoteAPI.create(title, content, category, priority, reminder_time, image_url)

    def upload_image(self, filepath: str):
        """Gọi UploadAPI để tải ảnh lên ImgBB và trả về kết quả."""
        return UploadAPI.upload_image(filepath)
