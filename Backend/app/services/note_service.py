from datetime import datetime
from app.schemas.note_schema import NoteCreateSchema
from app.repositories.note_repository import NoteRepository


class NoteService:
    def __init__(self):
        self.note_repo = NoteRepository()

    def create_note(self, note_data: NoteCreateSchema, user_id: str = None):
        data = note_data.dict()
        data["create_at"] = datetime.now()
        data["update_at"] = datetime.now()
        data["user_id"] = note_data.user_id or user_id

        if not data.get("user_id"):
            raise ValueError("user_id is required")

        note_id = self.note_repo.create_note(data)
        return {
            "id": note_id,
            "message": "Tạo ghi chú thành công"
        }

    def get_notes_by_user(self, user_id: str):
        return self.note_repo.get_notes_by_user(user_id)

    def search_notes_by_user(self, user_id: str, keyword: str):
        return self.note_repo.search_notes_by_user(user_id, keyword)

    def update_note(self, note_id: str, note_data: NoteCreateSchema):
        update_data = note_data.dict(exclude_unset=True)
        if not update_data:
            return {"message": "Không có dữ liệu để cập nhật"}
        self.note_repo.update_note(note_id, update_data)
        return {"message": "Cập nhật ghi chú thành công"}

    def delete_note(self, note_id: str):
        deleted_count = self.note_repo.delete_note(note_id)
        return {
            "deleted_count": deleted_count,
            "message": "Xóa ghi chú thành công" if deleted_count else "Không tìm thấy ghi chú"
        }