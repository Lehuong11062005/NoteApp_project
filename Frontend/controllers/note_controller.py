from Frontend.services.note_api import NoteAPI
from Frontend.models.note import Note


class NoteController:
    def __init__(self, username: str = None):
        self.username = username

    def get_notes(self):
        success, data = NoteAPI.get_all(self.username)
        if success:
            notes = []
            for item in data:
                create_at = item.get("create_at", "")[:10] if item.get("create_at") else ""
                note = Note(
                    id=item.get("_id"), title=item.get("title", "No Title"),
                    content=item.get("content", ""), category=item.get("category", ""),
                    priority=item.get("priority", ""), create_at=create_at
                )
                notes.append(note)
            return True, notes
        return False, data

    def get_statistics(self, period="day"):
        success, data = NoteAPI.get_statistics(self.username, period)
        if success:
            return True, [
                (item.get("date", ""), item.get("count", 0))
                for item in data
            ]
        return False, data

    def create_note(self, title, content, category, priority, reminder_time=None, image_url=None):
        if not title or not content:
            return False, "Tiêu đề và nội dung không được để trống!"
        return NoteAPI.create_note(
            title,
            content,
            category,
            priority,
            reminder_time,
            image_url,
            user_id=self.username,
        )