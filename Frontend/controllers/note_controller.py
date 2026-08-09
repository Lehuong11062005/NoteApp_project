from typing import List, Optional, Tuple, Union
from Frontend.models.note import Note
from Frontend.services.note_api import NoteAPI


class NoteController:
    def __init__(self, username: Optional[str] = None):
        self.username = username

    def get_notes(self) -> Tuple[bool, Union[List[Note], str]]:
        """Lấy danh sách các ghi chú của người dùng."""
        success, data = NoteAPI.get_all(self.username)
        if success:
            notes = []
            if isinstance(data, list):
                for item in data:
                    create_at = (
                        item.get("create_at", "")[:10]
                        if item.get("create_at")
                        else ""
                    )
                    note = Note(
                        id=item.get("_id"),
                        title=item.get("title", "No Title"),
                        content=item.get("content", ""),
                        category=item.get("category", ""),
                        priority=item.get("priority", ""),
                        create_at=create_at,
                    )
                    notes.append(note)
            return True, notes
        return False, data or "Không thể tải danh sách ghi chú"

    def create_note(
        self,
        title: str,
        content: str,
        category: str,
        priority: str,
        reminder_time: Optional[str] = None,
        image_url: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """Tạo ghi chú mới."""
        if not title or not content:
            return False, "Tiêu đề và nội dung không được để trống!"

        return NoteAPI.create_note(
            title=title,
            content=content,
            category=category,
            priority=priority,
            reminder_time=reminder_time,
            image_url=image_url,
            user_id=self.username,
        )

    def update_note(
        self,
        note_id: str,
        title: str,
        content: str,
        category: str,
        priority: str,
        reminder_time: Optional[str] = None,
        image_url: Optional[str] = None,
    ) -> Tuple[bool, str]:
        """Cập nhật thông tin ghi chú."""
        if not note_id:
            return False, "Không tìm thấy ghi chú để cập nhật!"
        if not title or not content:
            return False, "Tiêu đề và nội dung không được để trống!"

        return NoteAPI.update_note(
            note_id=note_id,
            title=title,
            content=content,
            category=category,
            priority=priority,
            reminder_time=reminder_time,
            image_url=image_url,
            user_id=self.username,
        )

    def delete_note(self, note_id: str) -> Tuple[bool, str]:
        """Xóa ghi chú theo ID."""
        if not note_id:
            return False, "ID ghi chú không hợp lệ!"

        return NoteAPI.delete_note(note_id)